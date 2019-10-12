from .error_core import ExperienceException
from .system_error import SystemError as SysError



class SystemException(ExperienceException):
    def __init__(self, error_obj=None, *context):
        if not error_obj:
            raise SystemException(110001, 'error_obj')

        if isinstance(error_obj, int):
            error = SysError(error_obj)
            self._error_code = error_obj
        elif isinstance(error_obj, str):
            error = Sys[error_obj]
            self._error_code = error.value
        elif isinstance(error_obj, SysError):
            error = error_obj
            self._error_code = error.value

        if context:
            super().__init__(error.desc_with_param(*context))
        else:
            super().__init__(error.desc)

    @property
    def error_code(self):
        return self._error_code
