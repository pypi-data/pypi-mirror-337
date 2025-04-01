from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from semantha_sdk.smartcluster.model.cluster import Cluster
from typing import List
from typing import Optional

@dataclass
class SourceDoc:
    """ author semantha, this is a generated class do not change manually! """
    document_id: Optional[str] = None
    clusters: Optional[List[Cluster]] = None

SourceDocSchema = class_schema(SourceDoc, base_schema=RestSchema)
