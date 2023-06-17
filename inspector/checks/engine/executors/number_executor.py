from . import CheckExecutor, Result


class NumberExecutor(CheckExecutor):
    def execute(self):
        return Result(value_type="number", number_value=getattr(self.datacheck, f"{self.side}_number_value"))
