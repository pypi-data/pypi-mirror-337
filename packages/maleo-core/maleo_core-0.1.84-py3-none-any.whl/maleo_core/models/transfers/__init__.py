from .payloads import BasePayloads
from .parameters import BaseParameters
from .results import BaseResults

class BaseTransfers:
    Payloads = BasePayloads
    Parameters = BaseParameters
    Results = BaseResults