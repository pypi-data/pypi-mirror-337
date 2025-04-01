from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from semantha_sdk.smartcluster.model.cluster_content import ClusterContent
from typing import List
from typing import Optional

@dataclass
class ClusterUpdate:
    """ author semantha, this is a generated class do not change manually! """
    number: Optional[int] = None
    name: Optional[str] = None
    content: Optional[List[ClusterContent]] = None
    summary: Optional[str] = None
    hidden: Optional[bool] = None

ClusterUpdateSchema = class_schema(ClusterUpdate, base_schema=RestSchema)
