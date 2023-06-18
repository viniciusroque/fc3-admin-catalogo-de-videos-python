from datetime import datetime
import unittest
from __seedwork.domain.exceptions import NotFoundException
from __seedwork.domain.repository import SearchResult
from __seedwork.domain.value_objects import UniqueEntityId
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository
from category.infra.repositories import InMemoryCategoryRepository


class TestCategoryRepository(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            CategoryRepository()

        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class CategoryRepository with "+
            "abstract methods delete, find_all, find_by_id, insert, search, update"
        )

    def test_sortable_fields(self):
        self.assertEqual(CategoryRepository.sortable_fields, [])



class TestInMemoryCategoryRepository(unittest.TestCase):

    repo: InMemoryCategoryRepository

    def setUp(self) -> None:
        self.repo = InMemoryCategoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = Category(name='Movie')
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw_not_found_exception_in_find_by_id(self):
        entity_id = '1'
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity_id)

        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID '{entity_id}'"
        )

        unique_entity_id = UniqueEntityId()
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)

        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID '{unique_entity_id}'"
        )

    def test_find_by_id(self):
        entity = Category(name='Test')
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity_found)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity_found)

    def test_find_all(self):
        entity = Category(name='Movie')
        self.repo.insert(entity)

        entities_found = self.repo.find_all()
        self.assertListEqual(entities_found, [entity])

    def test_throw_not_found_exception_in_update(self):
        entity = Category(name='Movie')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)

        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID '{entity.id}'"
        )

    def test_update(self):
        entity = Category(name='Movie')
        self.repo.insert(entity)

        entity_updated = Category(
            unique_entity_id=entity.unique_entity_id,
            name='Movie  Updated',
            description='some description'
        )
        self.repo.update(entity_updated)
        self.assertEqual(self.repo.items[0], entity_updated)

    def test_delete(self):
        entity = Category(name='Movie')
        self.repo.insert(entity)

        self.repo.delete(entity.id)
        self.assertListEqual(self.repo.items, [])

        entity = Category(name='Movie')
        self.repo.insert(entity)

        self.repo.delete(entity.unique_entity_id)
        self.assertListEqual(self.repo.items, [])

    def test_throw_not_found_exception_in_delete(self):
        entity_id = '1'
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity_id)

        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID '{entity_id}'"
        )

        unique_entity_id = UniqueEntityId()
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(unique_entity_id)

        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID '{unique_entity_id}'"
        )


    def test__apply_filter(self):
        items = [Category(name='Movie')]
        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, None)
        self.assertEqual(result, items)

        items = [
            Category(name='test'),
            Category(name='TEST'),
            Category(name='fake'),
            Category(name='_test_'),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, 'TEST')
        self.assertEqual(result, [items[0], items[1], items[3]])

        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, '5')
        self.assertEqual(result, [])

    def test__apply_sort(self):
        items = [
            Category(name='b', created_at=datetime(2023, 6, 18, 1, 0, 0)),
            Category(name='a', created_at=datetime(2023, 6, 18, 1, 0, 1)),
            Category(name='c', created_at=datetime(2022, 6, 18, 2, 0, 0)),
        ]

       # pylint: disable=protected-access
        result = self.repo._apply_sort(items, 'name', None)
        self.assertEqual(result, [items[1], items[0], items[2]])

       # pylint: disable=protected-access
        result = self.repo._apply_sort(items, 'name', 'asc')
        self.assertEqual(result, [items[1], items[0], items[2]])

       # pylint: disable=protected-access
        result = self.repo._apply_sort(items, 'name', 'desc')
        self.assertEqual(result, [items[2], items[0], items[1]])

       # pylint: disable=protected-access
        result = self.repo._apply_sort(items, 'created_at', 'asc')
        self.assertEqual(result, [items[2], items[0], items[1]])

        result = self.repo._apply_sort(items, 'created_at', 'desc')
        self.assertEqual(result, [items[1], items[0], items[2]])

        # pylint: disable=protected-access
        result = self.repo._apply_sort(items)
        self.assertEqual(result, [items[2], items[0], items[1]])


    def test__apply_paginate(self):
        items = [
            Category(name='a'),
            Category(name='b'),
            Category(name='c'),
            Category(name='d'),
            Category(name='e'),
        ]

       # pylint: disable=protected-access
        result = self.repo._apply_paginate(items, 1, 2)
        self.assertEqual(result, [items[0], items[1]])

       # pylint: disable=protected-access
        result = self.repo._apply_paginate(items, 2, 2)
        self.assertEqual(result, [items[2], items[3]])

       # pylint: disable=protected-access
        result = self.repo._apply_paginate(items, 3, 2)
        self.assertEqual(result, [items[4]])

       # pylint: disable=protected-access
        result = self.repo._apply_paginate(items, 4, 2)
        self.assertEqual(result, [])

    def test_search_when_params_is_empty(self):
        entity = Category(name='a')
        items = [entity] * 16
        self.repo.items = items

        result = self.repo.search(self.repo.SearchParams())
        self.assertEqual(
            result,
            SearchResult(
                items=[entity] * 15,
                total=16,
                current_page=1,
                per_page=15,
                sort=None,
                sort_dir=None,
                filter=None
            )
        )

    def test_search_applying_filter_and_paginate(self):
        items = [
            Category(name='test'),
            Category(name='a'),
            Category(name='TEST'),
            Category(name='TeSt'),
        ]

        self.repo.items = items
        result = self.repo.search(self.repo.SearchParams(
            page=1,
            per_page=2,
            filter='TEST'
        ))

        self.assertEqual(
            result,
            SearchResult(
                items=[items[0], items[2]],
                total=3,
                current_page=1,
                per_page=2,
                sort=None,
                sort_dir=None,
                filter='TEST'
            )
        )

        result = self.repo.search(self.repo.SearchParams(
            page=2,
            per_page=2,
            filter='TEST'
        ))

        self.assertEqual(
            result,
            SearchResult(
                items=[items[3]],
                total=3,
                current_page=2,
                per_page=2,
                sort=None,
                sort_dir=None,
                filter='TEST'
            )
        )

        result = self.repo.search(self.repo.SearchParams(
            page=3,
            per_page=2,
            filter='TEST'
        ))

        self.assertEqual(
            result,
            SearchResult(
                items=[],
                total=3,
                current_page=3,
                per_page=2,
                sort=None,
                sort_dir=None,
                filter='TEST'
            )
        )

    def test_search_applying_sort_and_paginate(self):
        items = [
            Category(name='b'),
            Category(name='a'),
            Category(name='d'),
            Category(name='e'),
            Category(name='c'),
        ]

        self.repo.items = items

        arrange_by_asc = [
            {
                'input': self.repo.SearchParams(
                    page=1, per_page=2, sort='name'
                ),
                'output': SearchResult(
                    items=[items[1], items[0]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None
                )
            },
            {
                'input': self.repo.SearchParams(
                    page=2, per_page=2, sort='name'
                ),
                'output': SearchResult(
                    items=[items[4], items[2]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None
                )
            },
            {
                'input': self.repo.SearchParams(
                    page=3, per_page=2, sort='name'
                ),
                'output': SearchResult(
                    items=[items[3]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None
                )
            }
        ]

        for index, item in enumerate(arrange_by_asc):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                item['output'],
                f"The output using sort_dir asc on index {index} is different"
            )

        arrange_by_desc = [
            {
                'input': self.repo.SearchParams(
                    page=1, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[3], items[2]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            },
            {
                'input': self.repo.SearchParams(
                    page=2, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[4], items[0]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            },
            {
                'input': self.repo.SearchParams(
                    page=3, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[1]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            }
        ]

        for index, item in enumerate(arrange_by_desc):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                item['output'],
                f"The output using sort_dir desc on index {index} is different"
            )

    def test_search_applying_filter_and_sort_and_paginate(self):
        items = [
            Category(name='test'),
            Category(name='a'),
            Category(name='TEST'),
            Category(name='e'),
            Category(name='TeSt'),
        ]
        self.repo.items = items

        result = self.repo.search(self.repo.SearchParams(
            page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        self.assertEqual(result, SearchResult(
            items=[items[2], items[4]],
            total=3,
            current_page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        result = self.repo.search(self.repo.SearchParams(
            page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        self.assertEqual(result, SearchResult(
            items=[items[0]],
            total=3,
            current_page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))
