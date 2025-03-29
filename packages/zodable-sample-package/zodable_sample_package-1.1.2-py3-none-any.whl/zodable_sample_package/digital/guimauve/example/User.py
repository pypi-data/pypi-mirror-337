from pydantic import BaseModel, Enum
from zodable_idschema import IdSchema
from zodable_sample_package_multiplatform import MultiplatformUserSchema
from uuid import UUID
from zodable_sample_package.digital.guimauve.example.Address import AddressSchema
from datetime import datetime

class UserSchema(BaseModel):
    id: UUID
    name: str
    email: str | None
    followers: int
    addresses: AddressSchema
    tags: str
    settings: str
    eventsByYear: int
    contactGroups: str
    createdAt: datetime
    externalUser: MultiplatformUserSchema
    birthDate: datetime
    otherId: IdSchema
