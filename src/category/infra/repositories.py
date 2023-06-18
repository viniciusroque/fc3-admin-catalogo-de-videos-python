from typing import List
from __seedwork.domain.repository import InMemorySearchableRepository
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository, InMemorySearchableRepository[Category, str]):
    sortable_fields: List[str] = ['name', 'created_at']

    def _apply_filter(self, items: List[Category], filter_param: str | None) -> List[Category]:
        if filter_param:
            return list(filter(
                lambda item: filter_param.lower() in item.name.lower(),
                items
            ))

        return items

    def _apply_sort(
            self,
            items: List[Category],
            sort: str = None,
            sort_dir: str = None
        ) -> List[Category]:

        if sort is None:
            sort = 'created_at'

        return super()._apply_sort(items, sort, sort_dir)
