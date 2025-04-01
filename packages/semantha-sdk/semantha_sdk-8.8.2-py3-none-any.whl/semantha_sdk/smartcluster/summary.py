from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.model.cluster_summary import ClusterSummary
from semantha_sdk.smartcluster.model.cluster_summary import ClusterSummarySchema

class SummaryEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings/{id}/clusters/{clusterid}/summary"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/summary"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def get(
        self,
    ) -> ClusterSummary:
        """
        
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.JSON)).execute().to(ClusterSummarySchema)

    
    
    
    