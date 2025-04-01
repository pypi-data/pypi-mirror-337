from enum import Enum

class ClusteringMin_cluster_size_typeEnum(str, Enum):
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH",
    
    def __str__(self) -> str:
        return self.value
