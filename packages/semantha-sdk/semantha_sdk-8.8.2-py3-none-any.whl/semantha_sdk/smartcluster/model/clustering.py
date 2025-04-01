from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from semantha_sdk.smartcluster.model.cluster import Cluster
from semantha_sdk.smartcluster.model.clustering_filter import ClusteringFilter
from semantha_sdk.smartcluster.model.notification import Notification
from semantha_sdk.smartcluster.model.plotly_chart import PlotlyChart
from semantha_sdk.smartcluster.model.source_doc import SourceDoc
from typing import Dict
from typing import List
from typing import Optional
from semantha_sdk.smartcluster.model.clustering_status_enum import ClusteringStatusEnum
from semantha_sdk.smartcluster.model.clustering_clustering_structure_enum import ClusteringClustering_structureEnum
from semantha_sdk.smartcluster.model.clustering_range_enum import ClusteringRangeEnum
from semantha_sdk.smartcluster.model.clustering_min_cluster_size_type_enum import ClusteringMin_cluster_size_typeEnum

@dataclass
class Clustering:
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str] = None
    name: Optional[str] = None
    status: Optional[ClusteringStatusEnum] = None
    created: Optional[int] = None
    recreated: Optional[int] = None
    min_cluster_size: Optional[str] = None
    notifications: Optional[List[Notification]] = None
    clustering_structure: Optional[ClusteringClustering_structureEnum] = None
    range: Optional[ClusteringRangeEnum] = None
    reduce_outliers: Optional[bool] = None
    umap_nr_of_neighbors: Optional[int] = None
    filter: Optional[ClusteringFilter] = None
    clusters: Optional[List[Cluster]] = None
    plotly: Optional[Dict[str, PlotlyChart]] = None
    min_cluster_size_type: Optional[ClusteringMin_cluster_size_typeEnum] = None
    source_docs: Optional[List[SourceDoc]] = None
    enable_gpt: Optional[bool] = None

ClusteringSchema = class_schema(Clustering, base_schema=RestSchema)
