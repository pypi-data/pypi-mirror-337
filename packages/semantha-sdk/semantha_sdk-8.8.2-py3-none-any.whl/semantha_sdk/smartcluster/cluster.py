from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.generatedname import GeneratednameEndpoint
from semantha_sdk.smartcluster.model.cluster import Cluster
from semantha_sdk.smartcluster.model.cluster import ClusterSchema
from semantha_sdk.smartcluster.model.cluster_update import ClusterUpdate
from semantha_sdk.smartcluster.model.cluster_update import ClusterUpdateSchema
from semantha_sdk.smartcluster.summary import SummaryEndpoint

class ClusterEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings/{id}/clusters/{clusterid}"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._clusterid}"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
        clusterid: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self._clusterid = clusterid
        self.__generatedname = GeneratednameEndpoint(session, self._endpoint)
        self.__summary = SummaryEndpoint(session, self._endpoint)

    @property
    def generatedname(self) -> GeneratednameEndpoint:
        return self.__generatedname

    @property
    def summary(self) -> SummaryEndpoint:
        return self.__summary

    
    
    def patch(
        self,
        body: ClusterUpdate
    ) -> Cluster:
        """
        
        """
        return self._session.patch(
            url=self._endpoint,
            json=ClusterUpdateSchema().dump(body)
        ).execute().to(ClusterSchema)

    def delete(
        self,
    ) -> None:
        """
        
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    