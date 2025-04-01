from enum import Enum

class ClusteringOverviewStatusEnum(str, Enum):
    QUEUED = "QUEUED",
    IN_PROGRESS = "IN_PROGRESS",
    FINISHED = "FINISHED",
    ERROR = "ERROR",
    CANCELLED = "CANCELLED",
    UPDATING = "UPDATING",
    SUMMARIZING = "SUMMARIZING",
    RENAMING = "RENAMING",
    
    def __str__(self) -> str:
        return self.value
