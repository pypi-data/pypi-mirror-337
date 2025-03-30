from __future__ import annotations
from maleo_core.models.base.transfers.results.general import BaseGeneralResults

class BaseServiceResults:
    Fail = BaseGeneralResults.Fail
    SingleData = BaseGeneralResults.SingleData
    MultipleData = BaseGeneralResults.MultipleData