from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.clusterings import ClusteringsEndpoint

class DomainEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._domainname}"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
        domainname: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self._domainname = domainname
        self.__clusterings = ClusteringsEndpoint(session, self._endpoint)

    @property
    def clusterings(self) -> ClusteringsEndpoint:
        return self.__clusterings

    
    
    
    
    