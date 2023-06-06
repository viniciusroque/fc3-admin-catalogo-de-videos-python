import unittest
from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass

from category.domain.entities import Category
from category.domain.exceptions import CategoryException


class TestCategoryUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):

        category = Category(name='Movie')
        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)

        created_at = datetime.now()
        category2 = Category(
            name='Movie',
            description='some description',
            is_active=False,
            created_at=created_at
        )
        self.assertEqual(category2.name, 'Movie')
        self.assertEqual(category2.description, 'some description')
        self.assertEqual(category2.is_active, False)
        self.assertEqual(category2.created_at, created_at)
        self.assertIsInstance(category2.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self):
        category1 = Category(name='Movie 1')
        category2 = Category(name='Movie 2')
        self.assertNotEqual(
            category1.created_at.timestamp(),
            category2.created_at.timestamp()
        )

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError) as assert_error:
            category = Category(name='test')
            category.name = 'fake name'

    def test_category_update_without_name(self):
        category = Category(name='test')
        with self.assertRaises(CategoryException) as assert_error:
            category.update(name='', description='')

        self.assertEqual(assert_error.exception.args[0], 'Name is required')

    def test_category_update_without_description(self):
        category = Category(name='test')
        with self.assertRaises(CategoryException) as assert_error:
            category.update(name='Name', description='')

        self.assertEqual(assert_error.exception.args[0], 'Description is required')

    def test_category_update(self):
        caterory = Category(name='test')

        name = 'Test updated'
        description = 'Description1'
        caterory.update(name=name, description=description)

        self.assertEqual(caterory.name, name)
        self.assertEqual(caterory.description, description)

    def test_category_activate(self):
        category = Category(name='test', is_active=False)

        self.assertFalse(category.is_active)
        category.activate()

        self.assertTrue(category.is_active)

    def test_category_desactivate(self):
        category = Category(name='test', is_active=True)

        self.assertTrue(category.is_active)
        category.desactivate()

        self.assertFalse(category.is_active)
