from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import Optional

@dataclass
class ClusterSize:
    """ author semantha, this is a generated class do not change manually! """
    min_type: Optional[str] = None
    min_value: Optional[int] = None

ClusterSizeSchema = class_schema(ClusterSize, base_schema=RestSchema)
