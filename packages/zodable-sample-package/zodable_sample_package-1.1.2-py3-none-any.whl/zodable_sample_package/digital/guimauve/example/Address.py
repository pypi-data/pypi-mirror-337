from pydantic import BaseModel, Enum
from zodable_sample_package.digital.guimauve.example.Country import CountrySchema

class AddressSchema(BaseModel):
    street: str
    city: str
    country: CountrySchema
