from pydantic import BaseModel, Enum

class MultiplatformTypeSchema(str, Enum):
    JVM = 'JVM'
    NATIVE = 'NATIVE'
    JS = 'JS'
