from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.bulk_clusters import BulkClustersEndpoint

class BulkEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings/{id}/bulk"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/bulk"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self.__clusters = BulkClustersEndpoint(session, self._endpoint)

    @property
    def clusters(self) -> BulkClustersEndpoint:
        return self.__clusters

    
    
    
    
    