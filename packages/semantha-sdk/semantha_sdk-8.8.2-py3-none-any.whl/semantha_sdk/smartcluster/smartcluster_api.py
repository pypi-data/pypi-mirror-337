from __future__ import annotations

from io import IOBase

from semantha_sdk.smartcluster.smartcluster import SmartclusterEndpoint
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint


class SmartclusterAPI(RestEndpoint):
    """ Entry point to the Smartcluster API.

        author semantha, this is a generated class do not change manually!
        Calls the /smartcluster,  endpoints.

        Note:
            The __init__ method is not meant to be invoked directly
            use `login()` with your credentials instead.
    """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__smartcluster = SmartclusterEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint

    @property
    def smartcluster(self) -> SmartclusterEndpoint:
        return self.__smartcluster

