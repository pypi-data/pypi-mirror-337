from enum import Enum

class NotificationTypeEnum(str, Enum):
    INFO = "INFO",
    WARNING = "WARNING",
    ERROR = "ERROR",
    GPT_BULK_SUMMARY_FAILED = "GPT_BULK_SUMMARY_FAILED",
    
    def __str__(self) -> str:
        return self.value
