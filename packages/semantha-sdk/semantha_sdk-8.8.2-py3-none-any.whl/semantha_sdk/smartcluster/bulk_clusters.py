from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from semantha_sdk.smartcluster.bulk_generatedname import BulkGeneratednameEndpoint
from semantha_sdk.smartcluster.bulk_summary import BulkSummaryEndpoint

class BulkClustersEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/smartcluster/domains/{domainname}/clusterings/{id}/bulk/clusters"
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
        self.__generatedname = BulkGeneratednameEndpoint(session, self._endpoint)
        self.__summary = BulkSummaryEndpoint(session, self._endpoint)

    @property
    def generatedname(self) -> BulkGeneratednameEndpoint:
        return self.__generatedname

    @property
    def summary(self) -> BulkSummaryEndpoint:
        return self.__summary

    
    
    
    
    