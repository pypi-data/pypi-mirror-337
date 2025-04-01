from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import Optional

@dataclass
class ClusterSummary:
    """ author semantha, this is a generated class do not change manually! """
    cluster_id: Optional[str] = None
    name: Optional[str] = None
    summary: Optional[str] = None

ClusterSummarySchema = class_schema(ClusterSummary, base_schema=RestSchema)
