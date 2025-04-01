from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.bulk import BulkEndpoint
from semantha_sdk.smartcluster.clusters import ClustersEndpoint
from semantha_sdk.smartcluster.model.clustering import Clustering
from semantha_sdk.smartcluster.model.clustering import ClusteringSchema
from semantha_sdk.smartcluster.model.clustering_overview import ClusteringOverview
from semantha_sdk.smartcluster.model.clustering_overview import ClusteringOverviewSchema
from semantha_sdk.smartcluster.model.clustering_update import ClusteringUpdate
from semantha_sdk.smartcluster.model.clustering_update import ClusteringUpdateSchema
from semantha_sdk.smartcluster.model.re_clustering import ReClustering
from semantha_sdk.smartcluster.model.re_clustering import ReClusteringSchema

class ClusteringEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings/{id}"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._id}"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
        id: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self._id = id
        self.__bulk = BulkEndpoint(session, self._endpoint)
        self.__clusters = ClustersEndpoint(session, self._endpoint)

    @property
    def bulk(self) -> BulkEndpoint:
        return self.__bulk

    @property
    def clusters(self) -> ClustersEndpoint:
        return self.__clusters

    def get(
        self,
        name: str = None,
        minprobability: int = None,
        maxprobability: int = None,
        createdafter: int = None,
        createdbefore: int = None,
        updatedafter: int = None,
        updatedbefore: int = None,
        tags: str = None,
        metadata: str = None,
        comment: str = None,
        documentclassids: str = None,
        recentlyadded: bool = None,
    ) -> Clustering:
        """
        
        Args:
        name str: 
    minprobability int: 
    maxprobability int: 
    createdafter int: 
    createdbefore int: 
    updatedafter int: 
    updatedbefore int: 
    tags str: 
    metadata str: 
    comment str: 
    documentclassids str: 
    recentlyadded bool: 
        """
        q_params = {}
        if name is not None:
            q_params["name"] = name
        if minprobability is not None:
            q_params["minprobability"] = minprobability
        if maxprobability is not None:
            q_params["maxprobability"] = maxprobability
        if createdafter is not None:
            q_params["createdafter"] = createdafter
        if createdbefore is not None:
            q_params["createdbefore"] = createdbefore
        if updatedafter is not None:
            q_params["updatedafter"] = updatedafter
        if updatedbefore is not None:
            q_params["updatedbefore"] = updatedbefore
        if tags is not None:
            q_params["tags"] = tags
        if metadata is not None:
            q_params["metadata"] = metadata
        if comment is not None:
            q_params["comment"] = comment
        if documentclassids is not None:
            q_params["documentclassids"] = documentclassids
        if recentlyadded is not None:
            q_params["recentlyadded"] = recentlyadded
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.JSON)).execute().to(ClusteringSchema)

    
    def patch(
        self,
        body: ClusteringUpdate
    ) -> ClusteringOverview:
        """
        
        """
        return self._session.patch(
            url=self._endpoint,
            json=ClusteringUpdateSchema().dump(body)
        ).execute().to(ClusteringOverviewSchema)

    def delete(
        self,
    ) -> None:
        """
        
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    def put(
        self,
        body: ReClustering
    ) -> ClusteringOverview:
        """
        
        """
        return self._session.put(
            url=self._endpoint,
            json=ReClusteringSchema().dump(body)
        ).execute().to(ClusteringOverviewSchema)
