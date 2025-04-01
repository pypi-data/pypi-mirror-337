from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.domains import DomainsEndpoint

class SmartclusterEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/smartcluster"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self.__domains = DomainsEndpoint(session, self._endpoint)

    @property
    def domains(self) -> DomainsEndpoint:
        return self.__domains

    
    
    
    
    