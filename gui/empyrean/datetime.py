from datetime import datetime
from pytz import timezone

from utils.private import default_timezone

class EmpyreanDateTime():
    datetime_format:    str
    date_time:          datetime

    date:               str
    time:               str

    time_zone:          timezone

    def __init__(self, location_timezone: str = '', generating_str: str ='', from_datetime: datetime =None) -> None:

        self.datetime_format = "%Y-%m-%d %H:%M"
        self.default_timezone = timezone(default_timezone)

        if location_timezone:
            self.time_zone = timezone(location_timezone)
        else:
            self.time_zone = self.default_timezone

        if generating_str:
            self.__convert_str_datetime_to_object(generating_str)
        elif from_datetime is not None:
            self.__convert_datetime_to_object(from_datetime)
        else:
            now_str = datetime.strftime(datetime.now(), self.datetime_format)
            self.date_time = datetime.strptime(now_str, self.datetime_format)
            self.date, self.time = now_str.split(' ')

    def __convert_str_datetime_to_object(self, generating_str: str)->None:
        if 'T' in generating_str:
            date_and_time, _, junk = generating_str.partition('+')
            date, _, time = date_and_time.partition('T')
            hour, minute, *unused_extra_precision = time.split(sep=':')
            generating_str = f'{date} {hour}:{minute}'
        
        self.date_time = self.time_zone.localize(datetime.strptime(generating_str, self.datetime_format))
        if (self.default_timezone == self.time_zone) == False:
            self.date_time = self.default_timezone.localize(self.date_time)
        self.date, self.time = datetime.strftime(self.date_time, self.datetime_format).split(' ')

    def __convert_datetime_to_object(self, original_datetime: datetime)->None:
        formatted_datetime_str = datetime.strftime(original_datetime, self.datetime_format)
        self.date_time = self.time_zone.localize(datetime.strptime(formatted_datetime_str, self.datetime_format))
        if (self.default_timezone == self.time_zone) == False:
            self.date_time = self.default_timezone.localize(self.date_time)
        self.date, self.time = datetime.strftime(self.date_time, self.datetime_format).split(' ')
    
    def as_string(self)->str:
        return datetime.strftime(self.date_time, self.datetime_format)