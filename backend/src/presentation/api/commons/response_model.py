from typing import Generic, TypeVar

from pydantic.generics import GenericModel

DataType = TypeVar("DataType")


class BaseResponseModel(GenericModel, Generic[DataType]):
    error: bool
    message: str
    data: DataType
