from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import Optional
from semantha_sdk.smartcluster.model.notification_type_enum import NotificationTypeEnum

@dataclass
class Notification:
    """ author semantha, this is a generated class do not change manually! """
    message: Optional[str] = None
    code: Optional[int] = None
    type: Optional[NotificationTypeEnum] = None
    timestamp: Optional[int] = None

NotificationSchema = class_schema(Notification, base_schema=RestSchema)
