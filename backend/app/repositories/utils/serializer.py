from pydantic import BaseModel


class Serializer:
    @staticmethod
    def serialize_to_dto(dto_cls: BaseModel, obj, *, from_attributes: bool = True):
        if isinstance(obj, dict):
            return dto_cls.model_construct(obj)
        return dto_cls.model_validate(obj, from_attributes=from_attributes)