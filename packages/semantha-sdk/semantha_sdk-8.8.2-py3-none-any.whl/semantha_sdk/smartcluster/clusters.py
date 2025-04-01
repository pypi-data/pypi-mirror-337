from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.cluster import ClusterEndpoint
from semantha_sdk.smartcluster.model.cluster import Cluster
from semantha_sdk.smartcluster.model.cluster import ClusterSchema
from typing import List

class ClustersEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings/{id}/clusters"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/clusters"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def __call__(
            self,
            clusterid: str,
    ) -> ClusterEndpoint:
        return ClusterEndpoint(self._session, self._endpoint, clusterid)

    def get(
        self,
    ) -> List[Cluster]:
        """
        
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.JSON)).execute().to(ClusterSchema)

    
    
    
    