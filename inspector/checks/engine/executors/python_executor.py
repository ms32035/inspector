from . import CheckExecutor
from ...constants import CHECK_TYPES


class PythonExecutor(CheckExecutor):
    supported_check_types = (CHECK_TYPES.NUMBER, CHECK_TYPES.STRING, CHECK_TYPES.DATE)

    def execute(self, check_logic):
        if self.check_type == CHECK_TYPES.STRING:
            return str(check_logic)
        if self.check_type == CHECK_TYPES.NUMBER:
            div = divmod(float(check_logic), 1)
            if div[1] == 0:
                return int(check_logic)
            return float(check_logic)
