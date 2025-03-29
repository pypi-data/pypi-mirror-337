import textwrap
from typing import List, Optional

from pandas import DataFrame
import relationalai as rai
from relationalai.early_access.dsl.ir.compiler import Compiler
from relationalai.early_access.dsl.ontologies.models import Model
from relationalai.early_access.rel.compiler import ModelToRel


class RelExecutor:

    @staticmethod
    def execute_model(model: Model, result_cols: Optional[List[str]] = None) -> DataFrame:
        compiler = Compiler()
        model_to_rel = ModelToRel()

        ir_model = compiler.compile_model(model)
        rel_model = str(model_to_rel.to_rel(ir_model))

        query_ir_model = compiler.compile_queries(model.queries)
        query_rel_model = str(model_to_rel.to_rel(query_ir_model, options={"no_declares": True}))

        return RelExecutor.execute(model.name, rel_model, query_rel_model, result_cols)

    @staticmethod
    def execute(database: str, rel_model: str, query: str, result_cols: Optional[List[str]] = None) -> DataFrame:
        """Executes Rel code using the RAI client."""

        resources = rai.clients.snowflake.Resources()
        resources.config.set("use_graph_index", False)

        try:
            resources.create_graph(database)
        except Exception as e:
            if "already exists" not in str(e).lower():
                raise e

        engine = resources.config.get("engine")
        rel_model = resources.create_models_code([("pyrel_qb_0", rel_model)])

        full_code = textwrap.dedent(f"""
            {rel_model}
            {query}
        """)

        results = resources.exec_raw(database, engine, full_code, False, nowait_durable=True)

        from relationalai.clients import result_helpers
        df, _ = result_helpers.format_results(results, None, result_cols)

        return df