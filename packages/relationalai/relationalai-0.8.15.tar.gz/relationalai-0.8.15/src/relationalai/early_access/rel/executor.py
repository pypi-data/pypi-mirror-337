from __future__ import annotations
import textwrap
import time

from pandas import DataFrame
from typing import Optional
import relationalai as rai

from relationalai import debugging
from relationalai.clients import result_helpers
from relationalai.early_access.metamodel import ir, compiler, executor as e, factory as f
from relationalai.early_access.rel import Compiler

class RelExecutor(e.Executor):
    """Executes Rel code using the RAI client."""

    def __init__(self, database: str, dry_run: bool = False) -> None:
        super().__init__()
        self.database = database
        self.dry_run = dry_run
        self.compiler = Compiler()
        self._resources = None
        self._last_model = None

    @property
    def resources(self):
        if not self._resources:
            with debugging.span("create_session"):
                start = time.perf_counter()
                self._resources = rai.clients.snowflake.Resources()
                self._resources.config.set("use_graph_index", False)
                try:
                    self._resources.create_graph(self.database)
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        raise e
                debugging.time("create_session", time.perf_counter() - start)
        return self._resources

    def execute(self, model: ir.Model, task:ir.Task, observer: Optional[compiler.Observer]=None) -> DataFrame:
        resources = self.resources

        with debugging.span("query") as end_span:
            start = time.perf_counter()
            rules_code = ""
            if self._last_model != model:
                with debugging.span("install_batch"):
                    rule_start = time.perf_counter()
                    rules_code = self.compiler.compile(model, observer)
                    debugging.time("install_batch", time.perf_counter() - rule_start, code=rules_code)
                    rules_code = resources.create_models_code([("pyrel_qb_0", rules_code)])
                    self._last_model = model

            task_model = f.compute_model(f.logical([task]))
            task_code = self.compiler.compile(task_model, observer, {"no_declares": True})

            full_code = textwrap.dedent(f"""
                {rules_code}
                {task_code}
            """)

            if self.dry_run:
                return DataFrame()

            engine = resources.config.get("engine")
            raw_results = resources.exec_raw(self.database, engine, full_code, False, nowait_durable=True)
            df, _ = result_helpers.format_results(raw_results, None)  # Pass None for task parameter
            end_span["results"] = df
            debugging.time("query", time.perf_counter() - start, df, code=task_code)
            return df
