from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from semantha_sdk.smartcluster.model.cluster import Cluster
from typing import List
from typing import Optional

@dataclass
class ClusteringUpdate:
    """ author semantha, this is a generated class do not change manually! """
    name: Optional[str] = None
    clusters: Optional[List[Cluster]] = None

ClusteringUpdateSchema = class_schema(ClusteringUpdate, base_schema=RestSchema)
