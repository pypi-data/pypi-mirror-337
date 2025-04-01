from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from semantha_sdk.smartcluster.model.cluster_size import ClusterSize
from semantha_sdk.smartcluster.model.clustering_filter import ClusteringFilter
from typing import List
from typing import Optional
from semantha_sdk.smartcluster.model.clustering_create_clustering_structure_enum import ClusteringCreateClustering_structureEnum
from semantha_sdk.smartcluster.model.clustering_create_range_enum import ClusteringCreateRangeEnum

@dataclass
class ClusteringCreate:
    """ author semantha, this is a generated class do not change manually! """
    name: str
    clustering_structure: Optional[ClusteringCreateClustering_structureEnum] = None
    reduce_outliers: Optional[bool] = None
    filter: Optional[ClusteringFilter] = None
    range: Optional[ClusteringCreateRangeEnum] = None
    umap_nr_of_neighbors: Optional[int] = None
    cluster_size: Optional[ClusterSize] = None
    tags: Optional[str] = None
    document_class_ids: Optional[List[str]] = None

ClusteringCreateSchema = class_schema(ClusteringCreate, base_schema=RestSchema)
