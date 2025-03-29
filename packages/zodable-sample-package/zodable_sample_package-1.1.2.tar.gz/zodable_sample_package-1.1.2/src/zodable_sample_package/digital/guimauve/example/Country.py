from pydantic import BaseModel, Enum

class CountrySchema(str, Enum):
    FRANCE = 'FRANCE'
    US = 'US'
