from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import List
from typing import Optional

@dataclass
class ClusteringFilter:
    """ author semantha, this is a generated class do not change manually! """
    tags: Optional[str] = None
    document_class_ids: Optional[List[str]] = None
    created_after: Optional[int] = None
    created_before: Optional[int] = None
    min_characters: Optional[int] = None

ClusteringFilterSchema = class_schema(ClusteringFilter, base_schema=RestSchema)
