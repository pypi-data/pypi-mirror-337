from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.clustering import ClusteringEndpoint
from semantha_sdk.smartcluster.model.clustering_create import ClusteringCreate
from semantha_sdk.smartcluster.model.clustering_create import ClusteringCreateSchema
from semantha_sdk.smartcluster.model.clustering_overview import ClusteringOverview
from semantha_sdk.smartcluster.model.clustering_overview import ClusteringOverviewSchema
from typing import List

class ClusteringsEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/clusterings"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def __call__(
            self,
            id: str,
    ) -> ClusteringEndpoint:
        return ClusteringEndpoint(self._session, self._endpoint, id)

    def get(
        self,
    ) -> List[ClusteringOverview]:
        """
        
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.JSON)).execute().to(ClusteringOverviewSchema)

    def post(
        self,
        body: ClusteringCreate = None,
    ) -> ClusteringOverview:
        """
        
        Args:
        body (ClusteringCreate): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=ClusteringCreateSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(ClusteringOverviewSchema)

    
    def delete(
        self,
    ) -> None:
        """
        
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    