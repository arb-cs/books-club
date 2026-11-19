from pydantic import BaseModel, ConfigDict


def to_camel(field_name: str) -> str:
    words = field_name.split("_")

    return words[0] + "".join(word.capitalize() for word in words[1:])


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        validate_by_alias=True,
    )
