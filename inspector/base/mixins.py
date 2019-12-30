class ExceptionCollectorMixin:
    def __init__(self):
        self._errors = []
        self.status: bool = True

    def add_exception(self, exc: Exception):
        self.status = False
        self._errors.append(repr(exc))

    def errors_text(self) -> str:
        return "\n".join(self._errors)
