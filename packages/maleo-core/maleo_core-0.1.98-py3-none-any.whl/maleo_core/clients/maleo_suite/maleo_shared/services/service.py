from maleo_core.models.base.transfers.results.clients.http import BaseHTTPClientResults
from maleo_core.clients.maleo_suite.maleo_shared.manager import MaleoSharedClientManager
from maleo_core.models.maleo_shared.transfers.parameters.client.service import MaleoSharedServiceClientParameters
from maleo_core.models.maleo_shared.transfers.parameters.general.service import MaleoSharedServiceGeneralParameters

class MaleoSharedServiceService:
    @staticmethod
    async def get_services(parameters:MaleoSharedServiceClientParameters.Get) -> BaseHTTPClientResults:
        """Fetch services from maleo-shared"""
        async with MaleoSharedClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSharedClientManager._base_url}/v1/services/"

            query_parameters = MaleoSharedServiceClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientResults(
                response=response,
                status_code=response.status_code,
                content=response.json(),
                success=response.is_success
            )

    @staticmethod
    async def get_service(parameters:MaleoSharedServiceGeneralParameters.GetSingle) -> BaseHTTPClientResults:
        """Fetch service from maleo-shared"""
        async with MaleoSharedClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSharedClientManager._base_url}/v1/services/"
            if parameters.identifier == MaleoSharedServiceGeneralParameters.GetSingleIdentifiers.ID:
                url += f"{parameters.value}"
            else:
                url += f"{parameters.identifier.value}/{parameters.value}"

            #* Construct query parameters
            params = {}
            if parameters.is_deleted is not None:
                params["is_deleted"] = str(parameters.is_deleted).lower()
            if parameters.is_active is not None:
                params["is_active"] = str(parameters.is_active).lower()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientResults(
                response=response,
                status_code=response.status_code,
                content=response.json(),
                success=response.is_success
            )