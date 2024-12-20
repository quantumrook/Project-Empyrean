from datetime import datetime
from pytz import timezone

class EmpyreanDateTime():
    datetime_format:    str
    date_time:          datetime

    date:               str
    time:               str

    time_zone:          timezone

    def __init__(self, location_timezone: str = '', api_string: str ='', from_datetime: datetime =None, from_string: str ='') -> None:

        self.datetime_format = "%Y-%m-%d %H:%M"

        if location_timezone:
            self.time_zone = timezone(location_timezone)
        else:
            self.time_zone = "America/Los_Angeles"

        if (api_string == '') == False:
            self.__convert_api_datetimes_to_object(api_string)
        
        if from_datetime is not None:
            self.__convert_datetime_to_object(from_datetime)
        
        if (from_string == '') == False:
            self.__convert_string_to_object(from_string)

    def __convert_api_datetimes_to_object(self, api_string: str, time_zone: str ='')->None:
        date_and_time, _, junk = api_string.partition("+")
        date, time = date_and_time.split(sep="T")
        hour, minute, *more_junk = time.split(sep=":")

        #Create the datetime object to handle timezone changing and formatting for us
        converted_datetime = datetime.strptime(f'{date} {hour}:{minute}', self.datetime_format)

        if time_zone:
            current_timezone = timezone(time_zone)
            converted_datetime = current_timezone.localize(current_timezone)
        converted_datetime = self.time_zone.localize(converted_datetime)

        self.date_time = converted_datetime
        self.date, self.time = converted_datetime.split(sep=" ")


    def __convert_datetime_to_object(self, original_datetime: datetime, time_zone: str ='')->None:
        """
        Assumes the provided datetime instance is already formatted to our specification
        """
        if time_zone:
            current_timezone = timezone(time_zone)
            converted_datetime = current_timezone.localize(current_timezone)
        converted_datetime = self.time_zone.localize(converted_datetime)
        self.date, self.time = datetime.strftime(self.date_time, self.datetime_format).split(' ')

    def __convert_string_to_object(self, generating_string: str, time_zone: str ='')->None:
        """
        Assumes the provided datetime instance is already formatted to our specification
        """
        self.date_time = self.time_zone.localize(datetime.strptime(generating_string, self.datetime_format))
        if time_zone:
            current_timezone = timezone(time_zone)
            self.date_time = current_timezone.localize(current_timezone)
        self.date, self.time = datetime.strftime(self.date_time, self.datetime_format).split(' ')
    
    def as_string(self)->str:
        return datetime.strftime(self.date_time, self.datetime_format)