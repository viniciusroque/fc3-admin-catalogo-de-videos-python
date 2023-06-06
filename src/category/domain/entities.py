from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from __seedwork.domain.entities import Entity
from category.domain.exceptions import CategoryException


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    # pylint: disable=unnecessary-lambda
    created_at: Optional[datetime] = field(
        default_factory=lambda:  datetime.now())

    def _validate(self) -> None:
        if len(self.name) == 0:
            raise CategoryException('Name is required')

        if len(self.description) == 0:
            raise CategoryException('Description is required')

    def update(self, name: str, description: str) -> None:
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        self._validate()

    def activate(self):
        object.__setattr__(self, 'is_active', True)

    def desactivate(self):
        object.__setattr__(self, 'is_active', False)
