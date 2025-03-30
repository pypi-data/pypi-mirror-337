from typing import Union
from maleo_core.clients.maleo_suite.maleo_shared.http.controllers.service import MaleoSharedServiceHTTPController
from maleo_core.models.maleo_shared.transfers.parameters.client.service import MaleoSharedServiceClientParameters
from maleo_core.models.maleo_shared.transfers.parameters.general.service import MaleoSharedServiceGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults

class MaleoSharedServiceHTTPService:
    @staticmethod
    async def get_services(parameters:MaleoSharedServiceClientParameters.Get) -> Union[BaseHTTPClientServiceResults.Fail, BaseHTTPClientServiceResults.MultipleData]:
        """Fetch services from maleo-shared"""
        result = await MaleoSharedServiceHTTPController.get_services(parameters=parameters)
        if not result.success:
            return BaseHTTPClientServiceResults.Fail.model_validate(result.model_dump())
        else:
            return BaseHTTPClientServiceResults.MultipleData.model_validate(result.model_dump())

    @staticmethod
    async def get_service(parameters:MaleoSharedServiceGeneralParameters.GetSingle) -> Union[BaseHTTPClientServiceResults.Fail, BaseHTTPClientServiceResults.SingleData]:
        """Fetch service from maleo-shared"""
        result = await MaleoSharedServiceHTTPController.get_services(parameters=parameters)
        if not result.success:
            return BaseHTTPClientServiceResults.Fail.model_validate(result.model_dump())
        else:
            return BaseHTTPClientServiceResults.SingleData.model_validate(result.model_dump())