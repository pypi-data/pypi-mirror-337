from pydantic import BaseModel
from enum import Enum

class MultiplatformTypeSchema(str, Enum):
    JVM = 'JVM'
    NATIVE = 'NATIVE'
    JS = 'JS'
