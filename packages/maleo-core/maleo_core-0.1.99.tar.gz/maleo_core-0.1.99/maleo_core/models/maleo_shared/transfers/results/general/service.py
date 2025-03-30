from typing import Optional
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.maleo_shared.transfers.results.query.service import MaleoSharedServiceQueryResults

class MaleoSharedServiceGeneralResults:
    class SingleData(BaseGeneralResults.SingleData):
        data:Optional[MaleoSharedServiceQueryResults.Get]

    class MultipleData(BaseGeneralResults.MultipleData):
        data:list[MaleoSharedServiceQueryResults.Get]