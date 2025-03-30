from . import constants as BaseConstants
from .exceptions import BaseExceptions
from .logger import Logger

class BaseUtils:
    Constants = BaseConstants
    Exceptions = BaseExceptions
    Logger = Logger