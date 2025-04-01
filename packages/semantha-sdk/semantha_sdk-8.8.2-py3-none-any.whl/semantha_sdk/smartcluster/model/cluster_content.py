from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import Optional

@dataclass
class ClusterContent:
    """ author semantha, this is a generated class do not change manually! """
    doc_id: Optional[str] = None
    probability: Optional[float] = None
    source_document_id: Optional[str] = None
    source_para_id: Optional[str] = None

ClusterContentSchema = class_schema(ClusterContent, base_schema=RestSchema)
