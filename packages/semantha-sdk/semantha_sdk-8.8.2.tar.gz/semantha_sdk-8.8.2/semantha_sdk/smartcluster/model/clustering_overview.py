from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from semantha_sdk.smartcluster.model.clustering_filter import ClusteringFilter
from semantha_sdk.smartcluster.model.notification import Notification
from typing import List
from typing import Optional
from semantha_sdk.smartcluster.model.clustering_overview_status_enum import ClusteringOverviewStatusEnum
from semantha_sdk.smartcluster.model.clustering_overview_clustering_structure_enum import ClusteringOverviewClustering_structureEnum
from semantha_sdk.smartcluster.model.clustering_overview_min_cluster_size_type_enum import ClusteringOverviewMin_cluster_size_typeEnum

@dataclass
class ClusteringOverview:
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str] = None
    name: Optional[str] = None
    status: Optional[ClusteringOverviewStatusEnum] = None
    created: Optional[int] = None
    recreated: Optional[int] = None
    size: Optional[int] = None
    min_cluster_size: Optional[str] = None
    notifications: Optional[List[Notification]] = None
    clustering_structure: Optional[ClusteringOverviewClustering_structureEnum] = None
    umap_nr_of_neighbors: Optional[int] = None
    min_cluster_size_type: Optional[ClusteringOverviewMin_cluster_size_typeEnum] = None
    filter: Optional[ClusteringFilter] = None

ClusteringOverviewSchema = class_schema(ClusteringOverview, base_schema=RestSchema)
