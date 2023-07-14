from datetime import datetime

from pytest_mock import MockerFixture

from src.common.helpers import DateHelper


def test_date_helper_now(mocker: MockerFixture):
    mock_now = mocker.patch(f'{DateHelper.__module__}.datetime')
    mock_now.now.return_value = datetime(2022, 8, 21)
    mock_now.side_effect = lambda *args, **kw: datetime(*args, **kw)

    assert DateHelper.now() == datetime(2022, 8, 21)


def test_date_helper_utcnow(mocker: MockerFixture):
    mock_now = mocker.patch(f'{DateHelper.__module__}.datetime')
    mock_now.utcnow.return_value = datetime(2022, 8, 21)
    mock_now.side_effect = lambda *args, **kw: datetime(*args, **kw)

    assert DateHelper.utcnow() == datetime(2022, 8, 21)


def test_date_helper_create():
    assert DateHelper.create(year=2022, month=12, day=5, hour=12, minute=30, second=0) == datetime(
        2022, 12, 5, 12, 30, 0
    )


def test_date_helper_add_to():
    date = DateHelper.create(2022, 12, 5)
    assert DateHelper.add_to(date, days=5, hours=2) == datetime(2022, 12, 10, 2)


def test_date_helper_subtract_from():
    date = DateHelper.create(2022, 12, 5)
    assert DateHelper.subtract_from(date, days=3, hours=3) == datetime(2022, 12, 1, 21)
