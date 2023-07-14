from dataclasses import dataclass
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from src.settings import get_settings


@dataclass
class DateHelper:
    settings = get_settings().future_data

    @staticmethod
    def now() -> datetime:
        """Get the datetime now"""
        return datetime.now()

    @staticmethod
    def utcnow() -> datetime:
        """Get the datetime utc now"""
        return datetime.utcnow()

    @staticmethod
    def add_to(date: datetime, days: int = 0, hours: int = 0) -> datetime:
        """Get the date with added time units."""
        return date + timedelta(days=days, hours=hours)

    @staticmethod
    def translate_month(month):
        translation_dict = {
            'Jan': 'Jan',
            'Feb': 'Fev',
            'Mar': 'Mar',
            'Apr': 'Abr',
            'May': 'Mai',
            'Jun': 'Jun',
            'Jul': 'Jul',
            'Aug': 'Ago',
            'Sep': 'Set',
            'Oct': 'Out',
            'Nov': 'Nov',
            'Dec': 'Dez',
        }
        return translation_dict.get(month, month)

    @staticmethod
    def subtract_from(date: datetime, days: int = 0, hours: int = 0) -> datetime:
        """Get the date with subtracted time units."""
        return date - timedelta(days=days, hours=hours)

    @staticmethod
    def create(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> datetime:
        """Create a new datetime"""
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def future_data(self) -> datetime:
        """Get the date for the next's months and days from today

        :return: DateTime months and days from today
        """
        return self.now() + relativedelta(months=self.settings.months, days=self.settings.days)
