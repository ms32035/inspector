from . import CheckExecutor, Result


class StringExecutor(CheckExecutor):
    def execute(self):
        return Result(value_type="string", string_value=getattr(self.datacheck, f"{self.side}_string_value"))
