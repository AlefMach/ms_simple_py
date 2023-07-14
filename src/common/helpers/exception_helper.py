import sys
import traceback
from types import TracebackType

ExcInfo = tuple[type[BaseException], BaseException, TracebackType]
OptExcInfo = ExcInfo | tuple[None, None, None]


class ExceptionHelper:
    @staticmethod
    def get_exc_info() -> OptExcInfo:
        error_type, error_value, trace = sys.exc_info()
        return error_type, error_value, trace

    @staticmethod
    def format_exception(exc_info: ExcInfo) -> list[str]:
        error_type, error_value, trace = exc_info
        return traceback.format_exception(error_type, error_value, trace)
