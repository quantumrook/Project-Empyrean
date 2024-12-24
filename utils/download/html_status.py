from enum import Enum

class HTMLStatusCode(Enum):
    OK                  = 200
    NOT_FOUND           = 404
    SERVICE_UNAVAILABLE = 503