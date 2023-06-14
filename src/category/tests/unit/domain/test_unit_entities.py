import unittest
from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass
from unittest.mock import patch

from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        with patch.object(Category, '_validate') as mock_validate_method:
            category = Category(name='Movie')
            mock_validate_method.assert_called_once()
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
        with patch.object(Category, '_validate') as mock_validate_method:
            category1 = Category(name='Movie 1')
            category2 = Category(name='Movie 2')

            mock_validate_method.assert_called()
            self.assertNotEqual(
                category1.created_at.timestamp(),
                category2.created_at.timestamp()
            )

    def test_is_immutable(self):
        with patch.object(Category, '_validate'):
            with self.assertRaises(FrozenInstanceError):
                category = Category(name='test')
                category.name = 'fake name'

    def test_update(self):
        with patch.object(Category, '_validate'):
            category = Category(name='test')

            name = 'Test updated'
            description = 'Description1'
            category.update(name=name, description=description)

            self.assertEqual(category.name, name)
            self.assertEqual(category.description, description)

    def test_activate(self):
        with patch.object(Category, '_validate'):
            category = Category(name='test', is_active=False)

            self.assertFalse(category.is_active)
            category.activate()

            self.assertTrue(category.is_active)

    def test_deactivate(self):
        with patch.object(Category, '_validate'):
            category = Category(name='test', is_active=True)

            self.assertTrue(category.is_active)
            category.deactivate()

            self.assertFalse(category.is_active)
