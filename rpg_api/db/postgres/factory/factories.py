import factory
from faker import Faker
from rpg_api import enums

from rpg_api.db.postgres.factory.async_base_factory import (
    AsyncSQLAlchemyModelFactory as AsyncFactory,
)
from rpg_api.utils import models
from typing import Any
from sqlalchemy import orm
from rpg_api.web.api.postgres.auth import auth_utils
from uuid import uuid4

fake = Faker()

CREATE = 1


class BaseUserFactory(AsyncFactory[models.BaseUser]):
    """Factory for BaseUser."""

    class Meta:
        model = models.BaseUser

    email = factory.LazyAttribute(lambda _: fake.email() + str(uuid4())[:7])
    password = auth_utils.hash_password("password")
    status = enums.UserStatus.active


class AbilityTypeFactory(AsyncFactory[models.AbilityType]):
    """Factory for AbilityType."""

    class Meta:
        model = models.AbilityType

    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())


class BaseClassFactory(AsyncFactory[models.BaseClass]):
    """Factory for BaseClass."""

    class Meta:
        model = models.BaseClass

    name = factory.LazyAttribute(lambda _: fake.name())


class AttributeFactory(AsyncFactory[models.Attribute]):
    """Factory for Attribute."""

    class Meta:
        model = models.Attribute

    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())


class PlaceFactory(AsyncFactory[models.Place]):
    """Factory for Place."""

    class Meta:
        model = models.Place

    name = factory.LazyAttribute(lambda _: fake.name())
    radius = 0.0
    x = 0
    y = 0


class RelationFactory(AsyncFactory[models.Relation]):
    """Factory for Relation."""

    _loads = [
        orm.joinedload(models.Relation.user1),
        orm.joinedload(models.Relation.user2),
    ]

    class Meta:
        model = models.Relation

    user1 = CREATE
    user2 = CREATE

    @classmethod
    async def _create_model(
        cls,
        model_class: type[AsyncFactory[models.Relation]],
        *args: Any,
        **kwargs: Any,
    ) -> AsyncFactory[models.Relation]:
        """Create model."""

        if kwargs["user1"] == CREATE:
            kwargs["user1"] = await BaseUserFactory.create()

        if kwargs["user2"] == CREATE:
            kwargs["user2"] = await BaseUserFactory.create()

        return await super()._create_model(model_class, *args, **kwargs)


class CharacterLocationFactory(AsyncFactory[models.CharacterLocation]):
    """Factory for CharacterLocation."""

    class Meta:
        model = models.CharacterLocation


class CharacterFactory(AsyncFactory[models.Character]):
    """Factory for Character."""

    _loads = [
        orm.joinedload(models.Character.base_class),
        orm.joinedload(models.Character.user),
        orm.joinedload(models.Character.character_location),
    ]

    class Meta:
        model = models.Character

    character_name = factory.LazyAttribute(lambda _: fake.name() + str(uuid4())[:7])

    base_class = CREATE
    character_location = CREATE
    user = CREATE

    @classmethod
    async def _create_model(
        cls,
        model_class: type[AsyncFactory[models.Character]],
        *args: Any,
        **kwargs: Any,
    ) -> AsyncFactory[models.Character]:
        """Create model."""

        if kwargs["base_class"] == CREATE:
            kwargs["base_class"] = await BaseClassFactory.create()

        if kwargs["user"] == CREATE:
            kwargs["user"] = await BaseUserFactory.create()

        if kwargs["character_location"] == CREATE:
            kwargs["character_location"] = await CharacterLocationFactory.create()

        return await super()._create_model(model_class, *args, **kwargs)


class AbilityFactory(AsyncFactory[models.Ability]):
    """Factory for Ability."""

    _loads = [
        orm.joinedload(models.Ability.ability_type),
    ]

    class Meta:
        model = models.Ability

    name = factory.LazyAttribute(lambda _: fake.name())
    ability_type = CREATE

    @classmethod
    async def _create_model(
        cls,
        model_class: type[AsyncFactory[models.Ability]],
        *args: Any,
        **kwargs: Any,
    ) -> AsyncFactory[models.Ability]:
        """Create model."""

        if kwargs["ability_type"] == CREATE:
            kwargs["ability_type"] = await AbilityTypeFactory.create()

        return await super()._create_model(model_class, *args, **kwargs)


class ClassAbilityFactory(AsyncFactory[models.ClassAbility]):
    """Factory for ClassAbility."""

    _loads = [
        orm.joinedload(models.ClassAbility.base_class),
        orm.joinedload(models.ClassAbility.ability),
    ]

    class Meta:
        model = models.ClassAbility

    base_class = CREATE
    ability = CREATE

    @classmethod
    async def _create_model(
        cls,
        model_class: type[AsyncFactory[models.ClassAbility]],
        *args: Any,
        **kwargs: Any,
    ) -> AsyncFactory[models.ClassAbility]:
        """Create model."""

        if kwargs["base_class"] == CREATE:
            kwargs["base_class"] = await BaseClassFactory.create()

        if kwargs["ability"] == CREATE:
            kwargs["ability"] = await AbilityFactory.create()

        return await super()._create_model(model_class, *args, **kwargs)


class CharacterAttributeFactory(AsyncFactory[models.CharacterAttribute]):
    """Factory for CharacterAttribute."""

    _loads = [
        orm.joinedload(models.CharacterAttribute.character),
        orm.joinedload(models.CharacterAttribute.attribute),
    ]

    class Meta:
        model = models.CharacterAttribute

    character = CREATE
    attribute = CREATE
    value = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))

    @classmethod
    async def _create_model(
        cls,
        model_class: type[AsyncFactory[models.CharacterAttribute]],
        *args: Any,
        **kwargs: Any,
    ) -> AsyncFactory[models.CharacterAttribute]:
        """Create model."""

        if kwargs["character"] == CREATE:
            kwargs["character"] = await CharacterFactory.create()

        if kwargs["attribute"] == CREATE:
            kwargs["attribute"] = await AttributeFactory.create()

        return await super()._create_model(model_class, *args, **kwargs)
