from __future__ import annotations
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
import re
from typing import Any, Sequence as PySequence
import itertools

from relationalai.early_access.metamodel import factory as f, ir, builtins, types
from relationalai.early_access.metamodel.util import OrderedSet, ordered_set
from relationalai.early_access.rel.executor import RelExecutor

#--------------------------------------------------
# Globals
#--------------------------------------------------

_global_id = itertools.count(0)

#--------------------------------------------------
# Root tracking
#--------------------------------------------------

_track_default = False
_track_roots = ContextVar('track_roots', default=_track_default)
_global_roots = ordered_set()

def _add_root(root):
    if _track_roots.get() or isinstance(root, Fragment):
        _global_roots.add(root)

def _remove_roots(items: PySequence[Producer|Fragment]):
    for item in items:
        if hasattr(item, "__hash__") and item.__hash__ and item in _global_roots:
            _global_roots.remove(item)

# decorator
def roots(enabled=_track_default):
    def decorator(func):
        def wrapper(*args, **kwargs):
            token = _track_roots.set(enabled)
            try:
                return func(*args, **kwargs)
            finally:
                _track_roots.reset(token)
        return wrapper
    return decorator

# with root_tracking(enabled=False): ...
@contextmanager
def root_tracking(enabled=_track_default):
    token = _track_roots.set(enabled)
    try:
        yield
    finally:
        _track_roots.reset(token)

#--------------------------------------------------
# Helpers
#--------------------------------------------------

def flatten(items:PySequence[Any]) -> list[Any]:
    flat = []
    for item in items:
        if isinstance(item, (list, tuple)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat

def find_subjects(items: PySequence[Producer]) -> set[Concept|Ref]:
    subjects = set()
    for item in items:
        if isinstance(item, Concept):
            subjects.add(item)
        elif isinstance(item, ConceptExpression):
            subjects.add(item._op)
        elif isinstance(item, Expression):
            subjects.update(find_subjects(item._params))
        elif isinstance(item, Ref):
            subjects.add(item)
        elif isinstance(item, Relationship) and item._parent:
            subjects.update(find_subjects([item._parent]))
    return subjects

def find_model(items: Any) -> Model|None:
    if isinstance(items, (list, tuple)):
        for item in items:
            if hasattr(item, "_model") and item._model:
                return item._model
    else:
        if hasattr(items, "_model") and items._model:
            return items._model
    return None

def find_keys(item: Any, keys:OrderedSet[Any]|None = None) -> OrderedSet[Any]:
    if keys is None:
        keys = ordered_set()
    if isinstance(item, (list, tuple)):
        for it in item:
            find_keys(it, keys)
    elif isinstance(item, Relationship) and item._parent:
        find_keys(item._parent, keys)
    elif isinstance(item, Concept):
        keys.add(item)
    elif isinstance(item, ConceptExpression):
        keys.add(item._op)
    elif isinstance(item, Ref):
        if isinstance(item._thing, Concept):
            keys.add(item._thing)
        else:
            find_keys(item._thing, keys)
    elif isinstance(item, Alias):
        find_keys(item._thing, keys)
    elif isinstance(item, Aggregate):
        find_keys(item._args, keys)
    elif isinstance(item, Expression):
        find_keys(item._params, keys)
    elif isinstance(item, BranchRef):
        find_keys(item._match, keys)
    elif isinstance(item, Match):
        pass
    elif isinstance(item, Distinct):
        pass
    elif isinstance(item, (str, int, float, bool)):
        pass
    else:
        raise ValueError(f"Cannot find keys for {item}")
    return keys

#--------------------------------------------------
# Producer
#--------------------------------------------------

class Producer:
    def __init__(self, model:Model|None) -> None:
        self._id = next(_global_id)
        self._model = model

    #--------------------------------------------------
    # Infix operator overloads
    #--------------------------------------------------

    def _bin_op(self, op, left, right) -> Expression:
        res = Concept.builtins["Number"].ref("res")
        return Expression(Relationship.builtins[op], left, right, res)

    def __add__(self, other):
        return self._bin_op("+", self, other)
    def __radd__(self, other):
        return self._bin_op("+", other, self)

    def __mul__(self, other):
        return self._bin_op("*", self, other)
    def __rmul__(self, other):
        return self._bin_op("*", other, self)

    def __sub__(self, other):
        return self._bin_op("-", self, other)
    def __rsub__(self, other):
        return self._bin_op("-", other, self)

    def __truediv__(self, other):
        return self._bin_op("/", self, other)
    def __rtruediv__(self, other):
        return self._bin_op("/", other, self)

    def __floordiv__(self, other):
        return self._bin_op("//", self, other)
    def __rfloordiv__(self, other):
        return self._bin_op("//", other, self)

    def __pow__(self, other):
        return self._bin_op("^", self, other)
    def __rpow__(self, other):
        return self._bin_op("^", other, self)

    def __mod__(self, other):
        return self._bin_op("%", self, other)
    def __rmod__(self, other):
        return self._bin_op("%", other, self)

    def __neg__(self):
        return self._bin_op("*", self, -1)

    #--------------------------------------------------
    # Filter overloads
    #--------------------------------------------------

    def _filter(self, op, left, right) -> Expression:
        return Expression(Relationship.builtins[op], left, right)

    def __gt__(self, other):
        return self._filter(">", self, other)
    def __ge__(self, other):
        return self._filter(">=", self, other)
    def __lt__(self, other):
        return self._filter("<", self, other)
    def __le__(self, other):
        return self._filter("<=", self, other)
    def __eq__(self, other) -> Any:
        return self._filter("=", self, other)
    def __ne__(self, other) -> Any:
        return self._filter("!=", self, other)

    #--------------------------------------------------
    # And/Or
    #--------------------------------------------------

    def __or__(self, other) -> Match:
        return Match(self, other)

    def __and__(self, other) -> Union:
        return Union(self, other)

    #--------------------------------------------------
    # getattr
    #--------------------------------------------------

    def __getattr__(self, name:str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"{type(self).__name__} has no attribute {name}")
        if not hasattr(self, "_relationships"):
            return super().__getattribute__(name)
        if name not in self._relationships:
            self._relationships[name] = Relationship(
                f"{{Any}} has {{{name}:Any}}",
                parent=self, prop_name=name, model=self._model
            )
        return self._relationships[name]

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif isinstance(value, Relationship):
            value._parent = self
            value._prop_name = name
            self._relationships[name] = value
        else:
            raise AttributeError(f"Cannot set attribute {name} on {type(self).__name__}")

    #--------------------------------------------------
    # ref + alias
    #--------------------------------------------------

    def ref(self, name:str|None=None) -> Ref:
        return Ref(self, name=name)

    def alias(self, name:str) -> Alias:
        return Alias(self, name)

    #--------------------------------------------------
    # Find model
    #--------------------------------------------------

    def _find_model(self, items:list[Any]) -> Model|None:
        if self._model:
            return self._model

        for item in items:
            if isinstance(item, (Producer, Fragment)) and item._model:
                self._model = item._model
                return item._model
        return None

    #--------------------------------------------------
    # Hash
    #--------------------------------------------------

    __hash__ = object.__hash__

    #--------------------------------------------------
    # _pprint
    #--------------------------------------------------

    def _pprint(self, indent:int=0) -> str:
        return str(self)

    #--------------------------------------------------
    # Fallbacks
    #--------------------------------------------------

    def select(self, *args: Any):
        raise NotImplementedError(f"`{type(self).__name__}.select` not implemented")

    def where(self, *args: Any):
        raise NotImplementedError(f"`{type(self).__name__}.where` not implemented")

    def require(self, *args: Any):
        raise NotImplementedError(f"`{type(self).__name__}.require` not implemented")

    def then(self, *args: Any):
        raise NotImplementedError(f"`{type(self).__name__}.then` not implemented")

#--------------------------------------------------
# Ref
#--------------------------------------------------

class Ref(Producer):
    def __init__(self, thing:Producer, name:str|None=None):
        super().__init__(thing._model)
        self._thing = thing
        self._name = name
        self._relationships = {}

    def __str__(self) -> str:
        if self._name:
            return f"{self._name}{self._id}"
        return f"{self._thing}{self._id}"

#--------------------------------------------------
# Concept
#--------------------------------------------------



class Concept(Producer):
    builtins = {}

    def __init__(self, name:str, extends:list[Any] = [], model:Model|None=None):
        super().__init__(model)
        self._name = name
        self._relationships = {}
        self._extends = []
        for e in extends:
            if isinstance(e, Concept):
                self._extends.append(e)
            elif python_types_to_concepts.get(e):
                self._extends.append(python_types_to_concepts[e])
            else:
                raise ValueError(f"Unknown concept {e} in extends")

    def when(self, *args: Any) -> Fragment:
        subjects = find_subjects(args)
        if len(subjects) == 0:
            raise ValueError("No subjects found in when clause")
        elif len(subjects) > 1:
            raise ValueError("Multiple subjects found in when clause")
        return where(*args).then(self(subjects.pop()))

    def require(self, *args: Any) -> Fragment:
        return where(self).require(*args)

    def _isa(self, other:Concept) -> bool:
        if self is other:
            return True
        for parent in self._extends:
            if parent._isa(other):
                return True
        return False

    def __call__(self, identity:Any=None, **kwargs: Any) -> Any:
        return ConceptExpression(self, identity, kwargs)

    def __str__(self):
        return self._name

#--------------------------------------------------
# Builtin Concepts
#--------------------------------------------------

Primitive = Concept.builtins["Primitive"] = Concept("Primitive")
Error = Concept.builtins["Error"] = Concept("Error")

# Load builtin types
for builtin in types.builtin_types:
    if isinstance(builtin, ir.ScalarType):
        Concept.builtins[builtin.name] = Concept(builtin.name, extends=[Primitive])

Decimal = Concept.builtins["Decimal"]

python_types_to_concepts = {
    int: Concept.builtins["Int"],
    float: Concept.builtins["Float"],
    str: Concept.builtins["String"],
    bool: Concept.builtins["Bool"],
}

#--------------------------------------------------
# Relationship
#--------------------------------------------------

@dataclass
class Field():
    name:str
    type_str:str
    is_many:bool = False

class Relationship(Producer):
    builtins = {}

    def __init__(self, madlib:Any, parent:Producer|None=None, prop_name:str="", model:Model|None=None, fields:list[Field]|None=None, ir_relation:ir.Relation|None=None):
        super().__init__(model or find_model(parent) or find_model(args))
        self._parent = parent
        self._madlib = madlib
        self._prop_name = prop_name
        self._relationships = {}
        self._fields:list[Field] = fields or self._parse_schema_format(madlib)
        self._ir_relation = ir_relation

    @property
    def _name(self):
        return self._prop_name or self._madlib

    def _parse_schema_format(self, format_string:str):
        # Pattern to extract fields like {Type*} or {name:Type*}
        pattern = r'\{([a-zA-Z0-9_]+)(\*?)(?::([a-zA-Z0-9_]+)(\*?))?\}'
        matches = re.findall(pattern, format_string)

        fields = []
        for field_name, field_name_is_many, field_type, field_type_is_many in matches:
            # If no type is specified, use the field name as the type
            if not field_type:
                field_type = field_name.lower()
                field_type_is_many = field_name_is_many

            fields.append(Field(field_name, field_type, bool(field_type_is_many)))

        return fields

    def __call__(self, *args: Any) -> Any:
        clean_args = list(args)
        if len(args) < len(self._fields):
            if self._parent:
                clean_args = [self._parent, *clean_args]
        return Expression(self, *clean_args)

    def __str__(self):
        if self._parent and self._prop_name:
            return f"{self._parent}.{self._prop_name}"
        return self._name

for builtin in builtins.builtin_relations:
    fields = []
    for field in builtin.fields:
        field_type = re.sub(r'[\]\}]', '*', re.sub(r'[\[\{\(]', '', str(field.type))).strip()
        fields.append(f"{field.name}:{field_type}")
    args = ' '.join([f"{{{f}}}"for f in fields])
    Relationship.builtins[builtin.name] =  Relationship(f"{builtin.name} {args}", parent=None, prop_name=builtin.name, ir_relation=builtin)

#--------------------------------------------------
# Expression
#--------------------------------------------------

infix_ops = ["+", "-", "*", "/", "//", "^", "%", ">", ">=", "<", "<=", "=", "!="]

class Expression(Producer):
    def __init__(self, op:Relationship|Concept, *params:Any):
        super().__init__(op._model or find_model(params))
        _add_root(self)
        _remove_roots(params)
        self._op = op
        self._params = params
        # self._source = runtime_env.get_source()

    def when(self, *args: Any) -> Fragment:
        return where(*args).then(self)

    def __str__(self):
        return f"({self._op} {' '.join(map(str, self._params))})"

    def _pprint(self, indent:int=0) -> str:
        if self._op._name in infix_ops:
            a, b = self._params[0], self._params[1]
            return f"{' ' * indent}{a} {self._op} {b}"
        return f"{' ' * indent}{self._op}({' '.join(map(str, self._params))})"

    def __getattr__(self, name: str):
        raise AttributeError(f"Expression has no attribute {name}")

class ConceptExpression(Expression):
    def __init__(self, con:Concept, identity:Any, kwargs:dict[str, Any]):
        super().__init__(con, identity, kwargs)

#--------------------------------------------------
# Aggregate
#--------------------------------------------------

class Aggregate(Producer):
    def __init__(self, op:Relationship, *args: Any):
        super().__init__(op._model or find_model(args))
        self._op = op
        self._args = args
        self._group = []
        self._where = where()

    def where(self, *args: Any) -> Aggregate:
        if not self._model:
            self._model = find_model(args)
        self._where = self._where.where(*args)
        return self

    def per(self, *args: Any) -> Aggregate:
        if not self._model:
            self._model = find_model(args)
        self._group = list(args)
        return self

    def __getattr__(self, name: str):
        raise AttributeError(f"Expression has no attribute {name}")

    def __str__(self):
        args = ', '.join(map(str, self._args))
        group = ', '.join(map(str, self._group))
        where = ""
        if group:
            group = f" (per {group})"
        if self._where._where:
            items = ', '.join(map(str, self._where._where))
            where = f" (where {items})"
        return f"({self._op} {args}{group}{where})"

class Group():
    def __init__(self, *args: Any):
        self._group = args

    def __str__(self):
        args = ', '.join(map(str, self._group))
        return f"(per {args})"

    #--------------------------------------------------
    # Agg funcs
    #--------------------------------------------------

    def count(self, *args: Any) -> Aggregate:
        return Aggregate(Relationship.builtins["count"], *args).per(*self._group)

    def sum(self, *args: Any) -> Aggregate:
        return Aggregate(Relationship.builtins["sum"], *args).per(*self._group)

    def avg(self, *args: Any) -> Aggregate:
        return Aggregate(Relationship.builtins["avg"], *args).per(*self._group)

    def min(self, *args: Any) -> Aggregate:
        return Aggregate(Relationship.builtins["min"], *args).per(*self._group)

    def max(self, *args: Any) -> Aggregate:
        return Aggregate(Relationship.builtins["max"], *args).per(*self._group)

#--------------------------------------------------
# Aggregate builtins
#--------------------------------------------------

def per(*args: Any) -> Group:
    return Group(*args)

def count(*args: Any) -> Aggregate:
    return Aggregate(Relationship.builtins["count"], *args)

def sum(*args: Any) -> Aggregate:
    return Aggregate(Relationship.builtins["sum"], *args)

def avg(*args: Any) -> Aggregate:
    return Aggregate(Relationship.builtins["avg"], *args)

def min(*args: Any) -> Aggregate:
    return Aggregate(Relationship.builtins["min"], *args)

def max(*args: Any) -> Aggregate:
    return Aggregate(Relationship.builtins["max"], *args)

#--------------------------------------------------
# Alias
#--------------------------------------------------

class Alias(Producer):
    def __init__(self, thing:Producer, name:str):
        super().__init__(thing._model)
        self._thing = thing
        self._name = name
        self._relationships = {}
        _remove_roots([thing])

    def __str__(self) -> str:
        return f"{self._thing} as {self._name}"

#--------------------------------------------------
# Match
#--------------------------------------------------

class BranchRef(Producer):
    def __init__(self, match:Match, ix:int):
        super().__init__(match._model)
        self._match = match
        self._ix = ix

    def __str__(self):
        return f"{self._match}#{self._ix}"

class Match(Producer):
    def __init__(self, *args: Any):
        super().__init__(find_model(args))
        self._args = list(self._flatten_args(args))
        if any(isinstance(arg, Fragment) and arg._is_effect() for arg in self._args):
            _add_root(self)
        _remove_roots(args)

        # check for validity
        is_select = None
        ret_count = 0
        for arg in self._args:
            if isinstance(arg, Fragment) and arg._is_effect():
                if is_select:
                    raise ValueError("Cannot mix expression and effect clauses in a match")
                is_select = False
            elif isinstance(arg, Fragment) and not arg._is_effect():
                if is_select is False:
                    raise ValueError("Cannot mix effect and expression clauses in a match")
                is_select = True
                if ret_count == 0:
                    ret_count = len(arg._select)
                elif ret_count != len(arg._select):
                    raise ValueError("All clauses must have the same number of return values")
            elif isinstance(arg, (str, int, float, bool)):
                if is_select is False:
                    raise ValueError("Cannot mix then and select clauses in a match")
                is_select = True
                if ret_count == 0:
                    ret_count = 1
                elif ret_count != 1:
                    raise ValueError("All clauses must have the same number of return values")
        self._is_select = is_select
        self._ret_count = ret_count

    def _flatten_args(self, args):
        for arg in args:
            if isinstance(arg, Match):
                for sub_arg in arg._args:
                    yield sub_arg
            else:
                yield arg

    def __iter__(self):
        for ix in range(self._ret_count):
            yield BranchRef(self, ix)

    def __str__(self):
        return " | ".join(map(str, self._args))

#---------------------------------------------/-----
# Union
#--------------------------------------------------

class Union(Match):
    def __str__(self):
        return " & ".join(map(str, self._args))

def union(*args: Any) -> Union:
    return Union(*args)

#--------------------------------------------------
# Quantifiers
#--------------------------------------------------

class Quantifier():
    def __init__(self, *args: Any):
        self._args = args
        self._model = find_model(args)
        _remove_roots(args)
        self._where = where()

    def where(self, *args: Any) -> Quantifier:
        if not self._model:
            self._model = find_model(args)
        self._where = self._where.where(*args)
        return self

class Exists(Quantifier):
    def __str__(self):
        args_str = ','.join(map(str, self._args))
        where_items = '\n        '.join(map(str, self._where._where))
        where = f"\n        {where_items}" if self._where._where else ""
        return f"(exists [{args_str}]{where})"

class Forall(Quantifier):
    def __str__(self):
        args_str = ','.join(map(str, self._args))
        where_items = '\n        '.join(map(str, self._where._where))
        where = f"\n        {where_items}" if self._where._where else ""
        return f"(forall [{args_str}]{where})"

class Not(Quantifier):
    def where(self, *args: Any) -> Quantifier:
        raise NotImplementedError("Not cannot have a where clause")

    def __str__(self):
        args_str = '\n    '.join(map(str, self._args))
        return f"(not {args_str})"

def exists(*args: Any) -> Exists:
    return Exists(*args)

def forall(*args: Any) -> Forall:
    return Forall(*args)

def not_(*args: Any) -> Not:
    return Not(*args)

#--------------------------------------------------
# Distinct
#--------------------------------------------------

class Distinct():
    def __init__(self, *args: Any):
        self._args = args
        self._model = find_model(args)
        _remove_roots(args)

def distinct(*args: Any) -> Distinct:
    return Distinct(*args)

#--------------------------------------------------
# Fragment
#--------------------------------------------------

class Fragment():
    def __init__(self, parent:Fragment|None=None, model:Model|None=None):
        self._id = next(_global_id)
        self._select = []
        self._where = []
        self._require = []
        self._then = []
        self._model = parent._model if parent else model
        self._parent = parent
        # self._source = runtime_env.get_source()
        if parent:
            self._select.extend(parent._select)
            self._where.extend(parent._where)
            self._require.extend(parent._require)
            self._then.extend(parent._then)

    def _add_items(self, items:PySequence[Any], to_attr:list[Any]):
        # TODO: ensure that you are _either_ a select, require, or then
        # not a mix of them
        if to_attr is self._then:
            _add_root(self)
        _remove_roots(items)
        to_attr.extend(items)
        if not self._model:
            self._model = find_model(items)
        return self

    def where(self, *args: Any) -> Fragment:
        f = Fragment(parent=self)
        return f._add_items(args, f._where)

    def select(self, *args: Any) -> Fragment:
        f = Fragment(parent=self)
        return f._add_items(args, f._select)

    def require(self, *args: Any) -> Fragment:
        f = Fragment(parent=self)
        return f._add_items(args, f._require)

    def then(self, *args: Any) -> Fragment:
        f = Fragment(parent=self)
        return f._add_items(args, f._then)

    #--------------------------------------------------
    # helpers
    #--------------------------------------------------

    def _is_effect(self) -> bool:
        return bool(self._then or (self._parent and self._parent._is_effect()))

    #--------------------------------------------------
    # And/Or
    #--------------------------------------------------

    def __or__(self, other) -> Match:
        return Match(self, other)

    def __and__(self, other) -> Union:
        return Union(self, other)

    #--------------------------------------------------
    # Stringify
    #--------------------------------------------------

    def __str__(self):
        sections = []
        if self._select:
            select = '\n    '.join(map(str, self._select))
            sections.append(f"(select\n    {select})")
        if self._where:
            where = '\n    '.join(map(str, self._where))
            sections.append(f"(where\n    {where})")
        if self._require:
            require = '\n    '.join(map(str, self._require))
            sections.append(f"(require\n    {require})")
        if self._then:
            effects = '\n    '.join(map(str, self._then))
            sections.append(f"(then\n    {effects})")

        return "\n".join(sections)

    #--------------------------------------------------
    # Execute
    #--------------------------------------------------

    def __iter__(self):
        # Iterate over the rows of the fragment's results
        return self.to_df().itertuples(index=False).__iter__()

    def inspect(self):
        # @TODO what format? maybe ignore row indices?
        print(self.to_df())

    def to_df(self):
        """Convert the fragment's results to a pandas DataFrame."""
        # @TODO currently this code assumes a Rel executor; should dispatch based on config
        if not self._model:
            raise ValueError("Cannot execute fragment without a model context")

        # from logscope import log
        # log(*self._model.rules)
        # log(self)

        qb_model = self._model or Model("anon")
        ir_model = qb_model._to_ir()
        query_task = qb_model._compiler.fragment(self)

        # log(*rule_tasks)
        # log(fragment_task)

        results = qb_model._to_executor().execute(ir_model, query_task)
        return results

#--------------------------------------------------
# Select / Where
#--------------------------------------------------

def select(*args: Any, parent:Fragment|None=None, model:Model|None=None) -> Fragment:
    return Fragment().select(*args)

def where(*args: Any, parent:Fragment|None=None, model:Model|None=None) -> Fragment:
    return Fragment().where(*args)

def require(*args: Any, parent:Fragment|None=None, model:Model|None=None) -> Fragment:
    return Fragment().require(*args)

def then(*args: Any, parent:Fragment|None=None, model:Model|None=None) -> Fragment:
    return Fragment().then(*args)

#--------------------------------------------------
# Model
#--------------------------------------------------

class Model():
    def __init__(self, name:str, dry_run: bool = False, implicit_effects:bool = False):
        self._id = next(_global_id)
        self.name = name
        self._dry_run = dry_run
        self.concepts:dict[str, Concept] = {}
        self.relationships:list[Relationship] = []
        if implicit_effects:
            _track_roots.set(True)

        # Compiler
        self._compiler = Compiler()
        self._prev_rule_count = 0
        self._last_compilation = None

        # Executor
        self._executor = None

    def _to_ir(self):
        if self._prev_rule_count == len(_global_roots) and self._last_compilation:
            return self._last_compilation
        self._last_compilation = self._compiler.model(self)
        return self._last_compilation

    def _to_executor(self):
        if not self._executor:
            self._executor = RelExecutor(self.name, dry_run=self._dry_run)
        return self._executor

    def Concept(self, name:str, extends:list[Concept|Any]=[]) -> Concept:
        if name not in self.concepts:
            self.concepts[name] = Concept(name, model=self, extends=extends)
        return self.concepts[name]

    def Relationship(self, *args) -> Relationship:
        return Relationship(*args, parent=None, prop_name="", model=self)

    def __enter__(self):
        self._token = _track_roots.set(True)

    def __exit__(self, exc_type, exc_value, traceback):
        _track_roots.reset(self._token)


#--------------------------------------------------
# Compile
#--------------------------------------------------

class CompilerContext():
    def __init__(self, compiler:Compiler, parent:CompilerContext|None=None):
        self.compiler = compiler
        self.parent = parent
        self.value_map:dict[Producer, ir.Value|list[ir.Var]] = parent.value_map.copy() if parent else {}
        self.items:OrderedSet[ir.Task] = OrderedSet()
        self.into_vars:list[ir.Var] = parent.into_vars.copy() if parent else []
        self.global_value_map:dict[Producer, ir.Value|list[ir.Var]] = parent.global_value_map if parent else {}

    def to_value(self, item:Producer) -> ir.Value|list[ir.Var]:
        if item not in self.value_map:
            if item in self.global_value_map:
                self.value_map[item] = self.global_value_map[item]
            else:
                name = item._name if hasattr(item, "_name") else "v"
                type = types.Any
                if isinstance(item, (Concept, Relationship)):
                    if isinstance(item, Relationship) and isinstance(item._parent, Concept):
                        name = f"{item._parent._name}_{name}"
                    if isinstance(item, ConceptExpression):
                        assert isinstance(item._op, Concept)
                        type = self.compiler.to_type(item._op)
                    elif isinstance(item, Concept):
                        type = self.compiler.to_type(item)
                name = name.lower()
                self.map_var(item, f.var(name, type))
        return self.value_map[item]

    def map_var(self, item:Producer, value:ir.Value|list[ir.Var]):
        self.global_value_map[item] = value
        self.value_map[item] = value

    def _has_item(self, item:ir.Task) -> bool:
        return bool(item in self.items or (self.parent and self.parent._has_item(item)))

    def add(self, item:ir.Task):
        if not self._has_item(item):
            self.items.add(item)

    def safe_wrap(self, required_hoists:PySequence[ir.VarOrElse]) -> ir.Task:
        first = self.items[0]
        if len(self.items) == 1 and isinstance(first, ir.Logical) and set(required_hoists).issubset(set(first.hoisted)):
            return self.items[0]
        return f.logical(list(self.items), required_hoists)

    def clone(self):
        return CompilerContext(self.compiler, self)


class Compiler():
    def __init__(self):
        self.types:dict[Concept, ir.ScalarType] = {}
        self.name_to_type:dict[str, ir.Type] = {}
        self.relations:dict[Relationship|Concept, ir.Relation] = {}

    #--------------------------------------------------
    # Type/Relation conversion
    #--------------------------------------------------

    def to_type(self, concept:Concept) -> ir.ScalarType:
        if concept not in self.types:
            if concept._name in types.builtin_scalar_types_by_name:
                self.types[concept] = types.builtin_scalar_types_by_name[concept._name]
            else:
                parent_types = [self.to_type(parent) for parent in concept._extends]
                self.types[concept] = f.scalar_type(concept._name, parent_types)
            self.name_to_type[concept._name] = self.types[concept]
        return self.types[concept]

    def to_relation(self, item:Concept|Relationship) -> ir.Relation:
        if item not in self.relations:
            if isinstance(item, Concept):
                fields = [f.field(item._name.lower(), self.to_type(item))]
                relation = f.relation(item._name, fields)
            elif isinstance(item, Relationship):
                if item._ir_relation:
                    relation = item._ir_relation
                else:
                    fields = [f.field(cur.name, types.Any) for cur in item._fields]
                    relation = f.relation(item._name, fields)
            self.relations[item] = relation
            return relation
        else:
            return self.relations[item]

    #--------------------------------------------------
    # Model
    #--------------------------------------------------

    @roots(enabled=False)
    def model(self, model:Model) -> ir.Model:
        rules = [self.compile_task(rule)
                 for rule in _global_roots
                 if not rule._model or rule._model == model]
        root = f.logical(rules)
        engines = ordered_set()
        relations = OrderedSet.from_iterable(self.relations.values())
        types = OrderedSet.from_iterable(self.types.values())
        return f.model(engines, relations, types, root)

    #--------------------------------------------------
    # Compile
    #--------------------------------------------------

    @roots(enabled=False)
    def compile_task(self, thing:Expression|Fragment) -> ir.Task:
        if isinstance(thing, (Expression, Match, Union)):
            return self.root_expression(thing)
        elif isinstance(thing, Fragment):
            return self.fragment(thing)

    #--------------------------------------------------
    # Root expression
    #--------------------------------------------------

    def root_expression(self, item:Expression) -> ir.Task:
        ctx = CompilerContext(self)
        self.update(item, ctx)
        return f.logical(list(ctx.items))

    #--------------------------------------------------
    # Fragment
    #--------------------------------------------------

    def fragment(self, fragment:Fragment, parent_ctx:CompilerContext|None=None, into_vars:list[ir.Var] = []) -> ir.Task:
        ctx = CompilerContext(self, parent_ctx)
        self.where(fragment._where, ctx)
        self.require(fragment._require, ctx)
        self.then(fragment._then, ctx)
        self.select(fragment._select, ctx)
        return f.logical(list(ctx.items), ctx.into_vars)

    def where(self, items:PySequence[Expression], ctx:CompilerContext):
        for item in items:
            self.lookup(item, ctx)

    def select(self, items:PySequence[Expression], ctx:CompilerContext):
        if not items:
            return

        fields = []
        for ix, item in enumerate(items):
            keys = find_keys(item)
            for key in keys:
                self.lookup(key, ctx)
            sub_ctx = ctx.clone()
            raw_v = self.lookup(item, sub_ctx)
            if not isinstance(raw_v, list):
                raw_v = [raw_v]
            if len(sub_ctx.items) >= 1:
                ctx.add(sub_ctx.safe_wrap([ir.Else(v, None) for v in raw_v if isinstance(v, ir.Var)]))

            for v in raw_v:
                name = f"v{len(fields)}"
                if isinstance(item, Alias):
                    name = item._name
                elif isinstance(v, ir.Var):
                    name = v.name
                if ctx.into_vars:
                    ctx.add(f.lookup(builtins.eq, [ctx.into_vars[ix], v]))
                else:
                    fields.append((name, v))
        if fields:
            ctx.add(f.output(fields))

    def require(self, items:PySequence[Expression], ctx:CompilerContext):
        for item in items:
            not_ctx = ctx.clone()
            self.lookup(item, not_ctx)
            not_body = f.logical(list(not_ctx.items))

            sub_ctx = ctx.clone()
            sub_ctx.add(f.not_(not_body))
            item_str = item._pprint() if isinstance(item, Producer) else str(item)
            self.update(Error(message=f"Requirement not met: {item_str}"), sub_ctx)
            ctx.add(f.logical(list(sub_ctx.items)))

    def then(self, items:PySequence[Expression], ctx:CompilerContext):
        for item in items:
            sub_ctx = ctx.clone()
            self.update(item, sub_ctx)
            if len(sub_ctx.items) > 1:
                ctx.add(f.logical(list(sub_ctx.items)))
            elif len(sub_ctx.items) == 1:
                ctx.add(sub_ctx.items[0])

    #--------------------------------------------------
    # Lookup
    #--------------------------------------------------

    def lookup(self, item:Any, ctx:CompilerContext) -> ir.Value|list[ir.Var]:

        if isinstance(item, Expression):
            relation = self.to_relation(item._op)
            params = [self.lookup(p, ctx) for p in item._params]
            ctx.add(f.lookup(relation, flatten(params)))
            return params[-1]

        elif isinstance(item, Concept):
            v = ctx.to_value(item)
            if not item._isa(Primitive):
                assert isinstance(v, ir.Var)
                relation = self.to_relation(item)
                ctx.add(f.lookup(relation, [v]))
            return v

        elif isinstance(item, Relationship):
            relation = self.to_relation(item)
            p = self.lookup(item._parent, ctx)
            v = ctx.to_value(item)
            assert isinstance(p, ir.Var) and isinstance(v, ir.Var)
            ctx.add(f.lookup(relation, [p, v]))
            # TODO handle non-binary
            return v

        elif isinstance(item, Ref):
            root = item._thing
            prev_mapping = ctx.to_value(root)
            out = ctx.to_value(item)
            ctx.map_var(root, out)
            self.lookup(root, ctx)
            ctx.map_var(root, prev_mapping)
            return out

        elif isinstance(item, Alias):
            return self.lookup(item._thing, ctx)

        elif isinstance(item, Aggregate):
            relation = self.to_relation(item._op)
            assert relation.fields[0].name == "projection", "Aggregate structure has changed"

            # group
            group = [self.lookup(g, ctx) for g in item._group]
            group = [item for item in flatten(group) if isinstance(item, ir.Var)]

            # Agg context
            agg_ctx = ctx.clone()
            out = agg_ctx.to_value(item)
            assert isinstance(out, ir.Var)

            # additional wheres
            self.where(item._where._where, agg_ctx)

            # raw_args
            arg_count = len(relation.fields) - 3 # skip projection, group, and result
            raw_args = flatten([self.lookup(a, agg_ctx) for a in item._args])

            # the projection includes all keys for the args
            projection = flatten([self.lookup(key, agg_ctx) for key in find_keys(item._args)])
            # the projection is also all raw_args that aren't consumed by the agg
            projection += raw_args[:-arg_count] if arg_count else raw_args
            projection = list(dict.fromkeys([item for item in projection if isinstance(item, ir.Var)]))

            # agg args + result var
            args = raw_args[-arg_count:] if arg_count else []
            args.append(out)

            # add the aggregation
            ir_agg = f.aggregate(relation, projection, group, args)
            if agg_ctx.items:
                internal = set(raw_args) - set(ctx.value_map.values())
                ctx.add(f.logical(list(agg_ctx.items), list([ir.Else(v, None) for v in internal])))
            ctx.add(ir_agg)
            return out

        elif isinstance(item, Not):
            not_ctx = ctx.clone()
            for a in item._args:
                self.lookup(a, not_ctx)
            ctx.add(f.not_(f.logical(list(not_ctx.items))))

        elif isinstance(item, Quantifier):
            agg_ctx = ctx.clone()
            self.where(item._where._where, agg_ctx)
            args = [self.lookup(a, agg_ctx) for a in item._args]
            args = [item for item in flatten(args) if isinstance(item, ir.Var)]
            body = f.logical(list(agg_ctx.items))
            if isinstance(item, Exists):
                ctx.add(f.exists(args, body))
            elif isinstance(item, Forall):
                ctx.add(f.for_all(args, body))

        elif isinstance(item, Fragment):
            sub_ctx = ctx.clone()
            ctx.add(self.fragment(item, sub_ctx))
            if len(ctx.into_vars) == 1:
                return ctx.into_vars[0]
            elif len(ctx.into_vars) > 1:
                return ctx.into_vars
            elif len(item._select) == 1:
                return sub_ctx.to_value(item._select[0])
            elif len(item._select) > 1:
                return flatten([sub_ctx.to_value(s) for s in item._select])

        elif isinstance(item, (Match, Union)):
            branches = []
            vars = []
            if item._is_select:
                vars = ctx.value_map.get(item)
                if not vars:
                    vars = [f.var(f"v{i}") for i in range(item._ret_count)]
                    ctx.map_var(item, vars)
                assert isinstance(vars, list)
                for branch in item._args:
                    branch_ctx = ctx.clone()
                    branch_ctx.into_vars = vars
                    v = self.lookup(branch, branch_ctx)
                    if not isinstance(v, list):
                        v = [v]
                    for var, ret in zip(vars, v):
                        if var is not ret:
                            branch_ctx.add(f.lookup(builtins.eq, [var, ret]))
                    branches.append(branch_ctx.safe_wrap(vars))
            else:
                for branch in item._args:
                    branch_ctx = ctx.clone()
                    self.update(branch, branch_ctx)
                    branches.append(branch_ctx.safe_wrap([]))
            if isinstance(item, Union):
                ctx.add(f.union(branches, vars))
            else:
                ctx.add(f.match(branches, vars))

        elif isinstance(item, BranchRef):
            vars = ctx.value_map.get(item._match)
            if not vars:
                self.lookup(item._match, ctx)
                vars = ctx.value_map.get(item._match)
            assert isinstance(vars, list)
            return vars[item._ix]

        elif isinstance(item, Group):
            for g in item._group:
                self.lookup(g, ctx)

        elif isinstance(item, Distinct):
            vs = [self.lookup(v, ctx) for v in item._args]
            return flatten(vs)

        elif isinstance(item, (int, float, str)):
            return item

        elif item is None:
            return None

        elif hasattr(item, "_compile_lookup"):
            return item._compile_lookup(self, ctx)

        else:
            raise ValueError(f"Cannot lookup {item}")

    #--------------------------------------------------
    # Update
    #--------------------------------------------------

    def update(self, item:Expression|Match|Union, ctx:CompilerContext) -> ir.Value|list[ir.Var]:
        if isinstance(item, ConceptExpression):
            assert isinstance(item._op, Concept)
            relation = self.to_relation(item._op)
            (ident, kwargs) = item._params
            out = ctx.to_value(item)
            rels = {self.to_relation(getattr(item._op, k)): self.lookup(v, ctx)
                    for k, v in kwargs.items()}
            if ident is not None:
                out = self.lookup(ident, ctx)
                ctx.map_var(item, out)
            else:
                out = ctx.to_value(item._op)
                assert isinstance(out, ir.Var)
                ctx.add(f.construct(out, rels))
            assert not isinstance(out, list)
            ctx.add(f.derive(relation, [out]))
            for k, v in rels.items():
                assert not isinstance(v, list)
                ctx.add(f.derive(k, [out, v]))
            return out

        elif isinstance(item, Expression):
            relation = self.to_relation(item._op)
            params = flatten([self.lookup(p, ctx) for p in item._params])
            ctx.add(f.derive(relation, params))
            return params[-1]

        elif isinstance(item, Fragment):
            self.lookup(item, ctx)

        elif isinstance(item, (Match, Union)):
            self.lookup(item, ctx)

        elif hasattr(item, "_compile_update"):
            return item._compile_update(self, ctx)

        else:
            raise ValueError(f"Cannot update {item}")

__all__ = ["select", "where", "require", "then", "distinct", "per", "count", "sum", "min", "max", "avg"]

#--------------------------------------------------
# Todo
#--------------------------------------------------
"""
- Syntax
    ✔ construct
    ✔ static data handling
    ✔ Fix fragments to not be chained
    ✔ Extends
    ✔  Quantifiers
        ✔ not
        ✔ exists
        ✔ forall
    ✔ Aggregates
    ✔ Require
    ✘ Multi-step chaining
    ✔ ref
    ✔ alias
    ✔ match
    ✔ union
    ✔ capture all rules
    ✔ implement aliasing
    ✔ support defining relationships via madlibs Relationship("{Person} was born on {birthday:Date}")
    ✔ distinct
    ☐ nested fragments
    ☐  handle relationships with multiple name fields being accessed via prop:
        Package.shipment = Relationship("{Package} in {Shipment} on {Date}")
        Package.shipment.date, Package.shipment.shipment, Package.shipment.package
    ☐  sources
        ☐  table
        ☐  csv

- Compilation
    ✔ simple expressions
    ✔ select
    ✔ then
    ✔ Quantifiers
        ✔ exists
        ✔ forall
        ✔ not
    ✔ Aggregates
        ✔ Determine agg keys from inputs
        ✔ Group
    ✔ Require
    ✔ Alias
    ✔ Ref
    ✔ Match
    ✔ Union
    ✔ whole model
    ✔ distinct
    ✔ add Else to hoists
    ☐ extends
        ☐ nominals
    ☐ have require find keys and return the keys in the error
    ☐ Match/union with multiple branch refs in a select, duplicates the whole match
    ☐ nested fragments

☐ Execution
    ✔ basic queries
    ✔ query when iterating over a select
    ☐ debugger hookup
    ☐ table sources

"""
