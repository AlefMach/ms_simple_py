from src.common.helpers import ExceptionHelper


def test_exception_helper_get_exc_info_should_succeed():
    try:
        raise Exception('Error')
    except Exception:
        error_type, error_value, _ = ExceptionHelper.get_exc_info()
        assert error_type, error_value == (Exception, Exception('Error'))


def test_exception_helper_get_exc_info_should_return_none():
    assert ExceptionHelper.get_exc_info() == (None, None, None)


def test_exception_helper_format_exception_should_succeed():
    try:
        raise Exception('Error')
    except Exception:
        exc_info = ExceptionHelper.get_exc_info()
        result = ExceptionHelper.format_exception(exc_info)
        assert result[0] == 'Traceback (most recent call last):\n'
        assert result.pop() == 'Exception: Error\n'
