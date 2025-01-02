"""Module used for encoding the HTML status codes monitored by
a RequestThread
"""
from enum import Enum

class HTMLStatusCode(Enum):
    """Helper Enum used for discussing the status response code from
    a RequestThread.
    """
    OK                  = 200
    NOT_FOUND           = 404
    SERVICE_UNAVAILABLE = 503
