from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import List
from typing import Optional

@dataclass
class ReClustering:
    """ author semantha, this is a generated class do not change manually! """
    documents: Optional[List[str]] = None

ReClusteringSchema = class_schema(ReClustering, base_schema=RestSchema)
