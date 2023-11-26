import uuid

from beanie import Document
from pydantic import BaseModel, Field

from ella_filtersapi import FilterFieldTypes

from src.documents import FilterableDocument



class SimpleDocument(Document):
    attribute: str = ""


class SubDocument(BaseModel):
    sub_attr: str = ""


class ComplexDocument(Document):
    sub: SubDocument
    attribute: str = ""


class DocumentWithDefaults(Document):
    required_attribute: str
    optional_attribute: str = "default"
    cached_attribute: str | None = None

    # @validator('required_param')
    # def validate_required_param(cls, v, values, **kwargs):
    #     assert v

    # def set_a(self, a):
    #     self.a = a


class MyDoc(Document):
    a: int = 0

    class Settings:
        name = "mydocs"


TEST_DOCUMENTS = [
    SimpleDocument,
    ComplexDocument,
    DocumentWithDefaults,
    MyDoc,
]
