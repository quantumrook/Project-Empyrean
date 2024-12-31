"""Module for wrapping python's built-in datetime around a series of helper functions."""
from datetime import datetime, timedelta
from typing import Self

from pytz import timezone
from utils.private.private import user_default_timezone


class EmpyreanDateTime():
    """Wrapper for python's built-in datetime module.
    """
    class Keys():
        """Helper class for maping dictionary keys to variables."""
        date: str = "date"
        time: str = "time"
        time_zone: str = "time_zone"

    datetime_format:    str      = "%Y-%m-%d %H:%M"
    default_timezone:   timezone = timezone(user_default_timezone)

    def __init__(self, location_timezone: str = '', today=False) -> None:

        self.date_time: datetime = None
        self.date: str           = ""
        self.time: str           = ""
        self.time_zone: timezone = EmpyreanDateTime.default_timezone

        if location_timezone:
            self.time_zone: timezone = timezone(location_timezone)

        if today:
            #default to now, for the case where nothing is given
            EmpyreanDateTime.__localize(datetime.now(), self)

    @staticmethod
    def __localize(original_dt: datetime, instance: Self) -> None:
        if not (EmpyreanDateTime.default_timezone == instance.time_zone):
            #localize and account for DST
            instance.date_time = instance.time_zone.localize(original_dt).astimezone(instance.time_zone)
            instance.date_time = instance.time_zone.normalize(instance.date_time)

            # ensure datetime_format
            generating_str = datetime.strftime(instance.date_time, EmpyreanDateTime.datetime_format)
            instance.date_time = datetime.strptime(generating_str, EmpyreanDateTime.datetime_format)
            instance.date, instance.time = generating_str.split(' ')
        else:
            generating_str = datetime.strftime(original_dt, EmpyreanDateTime.datetime_format)
            instance.date_time = datetime.strptime(generating_str, EmpyreanDateTime.datetime_format)
            instance.date, instance.time = generating_str.split(' ')

    @staticmethod
    def from_API(generating_str: str, location_timezone: str = '', is_expiration: bool = False) -> Self:
        """Converts the API date and time string to a version that we can better work with

        Args:
            generating_str (str): The API string.
            location_timezone (str, optional): The location's timezone, used for localizing. Defaults to ''.
            is_expiration (bool, optional): If the string contains additional information, its used to
            calculate and return a datetime for the end of this range. Defaults to False.

        Returns:
            Self: an EmpyreanDateTime built from the generating string.
        """
        new_instance = EmpyreanDateTime(location_timezone)

        date_and_time, _, expiration_data = generating_str.partition('+') #TODO :: use this to better set the expiration time for extended forecasts
        date, _, time = date_and_time.partition('T')
        hour, minute, *unused_extra_precision = time.split(sep=':')
        generating_str = f'{date} {hour}:{minute}'

        EmpyreanDateTime.__localize(datetime.strptime(generating_str, EmpyreanDateTime.datetime_format), new_instance)
        if is_expiration:
            new_instance = EmpyreanDateTime.add_days(new_instance, 7)
        return new_instance

    @staticmethod
    def from_Empyrean(datetime_data: dict[str, str]) -> Self:
        """Converts a JSON friendly dictionary of datetime data to an EmpyreanDateTime object.

        Args:
            datetime_data (dict[str, str]): The information used to populate the object.

        Returns:
            Self: A newly instantiated object.
        """
        new_instance = EmpyreanDateTime(datetime_data[EmpyreanDateTime.Keys.time_zone])
        generating_str = f'{datetime_data[EmpyreanDateTime.Keys.date]} {datetime_data[EmpyreanDateTime.Keys.time]}'

        EmpyreanDateTime.__localize(datetime.strptime(generating_str, EmpyreanDateTime.datetime_format), new_instance)
        return new_instance

    @staticmethod
    def from_datetime(original_datetime: datetime) -> Self:
        """Helper method for creating an EmpyreanDateTime when a python datetime object
        already exists.

        Args:
            original_datetime (datetime): The datetime to wrap.

        Returns:
            Self: A wrapped datetime.
        """
        new_instance = EmpyreanDateTime()
        EmpyreanDateTime.__localize(original_datetime, new_instance)
        return new_instance

    def as_string(self)->str:
        """Returns the date and time as a string according to the program formatting."""
        return datetime.strftime(self.date_time, self.datetime_format)

    def to_dict(self) -> dict[str, str]:
        """Helper function for preparing the object to be saved in a JSON format."""
        return {
            EmpyreanDateTime.Keys.date : self.date,
            EmpyreanDateTime.Keys.time : self.time,
            EmpyreanDateTime.Keys.time_zone : str(self.time_zone)
        }

    @staticmethod
    def is_in_range(questionable_datetime: Self, starting_datetime: Self, ending_datetime: Self) -> bool:
        """Helper function for returning whether the corresponding EmpyreanDateTime falls inside the specified range."""
        if questionable_datetime.date_time >= starting_datetime.date_time and questionable_datetime.date_time <= ending_datetime.date_time:
            return True
        return False

    @staticmethod
    def add_days(empyrean_datetime: Self, days: int) -> Self:
        """Create a new instance of EmpyreanDateTime but with 'days' into the future."""
        return EmpyreanDateTime.from_datetime(empyrean_datetime.date_time + timedelta(days=days))

    def hour(self) -> str:
        """Helper function for just returning the hour of the current object."""
        return self.time.split(":")[0]

TODAY = EmpyreanDateTime(today=True)
