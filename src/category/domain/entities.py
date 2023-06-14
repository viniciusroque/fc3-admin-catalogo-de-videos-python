from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import EntityValidationException
# from __seedwork.domain.validators import ValidatorRules #NOSONAR
from category.domain.validators import CategoryValidatorFactory


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    # pylint: disable=unnecessary-lambda
    created_at: Optional[datetime] = field(
        default_factory=lambda:  datetime.now())

    def __post_init__(self):
        if not self.created_at:
            self._set('created_at', datetime.now())

        self._validate()

    def update(self, name: str, description: str) -> None:
        self._set('name', name)
        self._set('description', description)
        self._validate()

    def activate(self):
        self._set('is_active', True)

    def deactivate(self):
        self._set('is_active', False)

    # def _validate(self) -> None: #NOSONAR
    #     ValidatorRules.values(self.name, 'name').required().string().max_length(255)
    #     ValidatorRules.values(self.description, 'description').string()
    #     ValidatorRules.values(self.is_active, 'is_active').boolean()

    def _validate(self) -> None:
        validator = CategoryValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)
