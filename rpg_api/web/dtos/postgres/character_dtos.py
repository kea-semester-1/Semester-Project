from pydantic import BaseModel
from uuid import UUID
from rpg_api.core.dtos.base_schemas import OrmBasicModel

from rpg_api.enums import Gender

from rpg_api.web.dtos.postgres.base_class_dtos import BaseClassSimpleDTO
from rpg_api.web.dtos.postgres.character_location_dtos import CharacterLocationSimpleDTO

from pydantic import Field


class CharacterDTO(OrmBasicModel):
    """Character DTO."""

    id: UUID
    base_class_id: UUID
    user_id: UUID
    character_location_id: UUID
    gender: Gender
    character_name: str
    alive: bool
    level: int
    xp: int
    money: int


class CharacterInputDTO(BaseModel):
    """Character input DTO."""

    base_class_id: int
    user_id: UUID
    gender: Gender
    character_name: str = Field(..., min_length=1, max_length=50)
    alive: bool = True
    level: int = 1
    xp: int = 1
    money: int = 1


class CharacterPartialInputDTO(BaseModel):
    """Character partial input DTO."""

    base_class_id: UUID
    gender: Gender
    character_name: str = Field(..., min_length=1, max_length=50)


class CharacterSimpleDTO(OrmBasicModel):
    """Character nested with class DTO."""

    id: UUID
    gender: Gender
    character_name: str
    alive: bool
    level: int
    xp: int
    money: int


class CharacterNestedWithClassAndLocationDTO(CharacterSimpleDTO):
    """Character nested with class and location DTO."""

    base_class: BaseClassSimpleDTO
    character_location: CharacterLocationSimpleDTO


class CharacterPlaceDTO(BaseModel):
    """Character place DTO."""

    id: UUID
    place: str


class CharacterUpdateDTO(BaseModel):
    """Character update DTO."""

    gender: Gender | None = None
    character_name: str | None = None
    alive: bool | None = None
    level: int | None = None
    xp: int | None = None
    money: int | None = None


class CharacterMoveInputDTO(BaseModel):
    """Character move input DTO."""

    x: int
    y: int
