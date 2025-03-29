from pydantic import BaseModel, Enum
from uuid import UUID
from zodable_sample_package_multiplatform.digital.guimauve.example.MultiplatformType import MultiplatformTypeSchema

class MultiplatformUserSchema(BaseModel):
    id: UUID
    type: MultiplatformTypeSchema
