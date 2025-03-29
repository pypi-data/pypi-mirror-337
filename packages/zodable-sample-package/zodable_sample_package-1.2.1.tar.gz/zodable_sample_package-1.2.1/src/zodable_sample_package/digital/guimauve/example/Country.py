from pydantic import BaseModel
from enum import Enum

class CountrySchema(str, Enum):
    FRANCE = 'FRANCE'
    US = 'US'
