from enum import Enum

class DownloadStatus(Enum):
    INSTANTIATING                   = 0
    INITIALIZING                    = 1
    BUILDING_REQUEST                = 2
    REQUEST_BUILT                   = 3
    API_TIMEOUT_PROTECTION_STARTED  = 4
    API_TIMEOUT_PROTECTION_COMPLETE = 5
    SENDING_REQUEST                 = 6
    REQUEST_RECIEVED                = 7
    CONVERTING_SOURCE_DATA          = 8
    REQUEST_FAILED                  = -1
    REQUEST_SUCCESS                 = 9
    SAVING_DATA                     = 10
    SAVE_COMPLETE                   = 11

    def max_value():
        return DownloadStatus.SAVE_COMPLETE.value

    def as_log_str(self):
        return self.name