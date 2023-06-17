from . import CheckExecutor, Result


class DateExecutor(CheckExecutor):
    def execute(self):
        return Result(value_type="date", date_value=getattr(self.datacheck, f"{self.side}_date_value"))
