from fast_depends.library import CustomField
from pydantic import BaseModel


class Payload(CustomField):
    def __init__(
        self, *, schema: BaseModel, cast: bool = True, required: bool = True
    ) -> None:
        super().__init__(cast=cast, required=required)

        self._schema = schema

    def use(self, **kwargs):
        kwargs = super().use(**kwargs)
        payload = kwargs[self.param_name]
        kwargs[self.param_name] = self._schema(**payload)

        return kwargs
