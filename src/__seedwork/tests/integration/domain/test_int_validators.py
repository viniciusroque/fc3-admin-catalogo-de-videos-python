import unittest

from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField

# pylint: disable=abstract-method
class StubSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()


class TestDRFValidatorIntegration(unittest.TestCase):

    def test_validation_with_error(self):
        validator = DRFValidator()
        serializer = StubSerializer(data={})
        is_valid = validator.validate(serializer)
        self.assertFalse(is_valid)
        self.assertEqual(
            validator.errors,
            {
                'name': ['This field is required.'],
                'price': ['This field is required.']
            }
        )

    def test_validation_without_error(self):
        validator = DRFValidator()
        serializer = StubSerializer(data={'name': 'Name 1', 'price': 5})
        is_valid = validator.validate(serializer)
        self.assertTrue(is_valid)
        self.assertEqual(
            validator.validated_data,
            {
                'name': 'Name 1',
                'price': 5
            }
        )

class TestStrictCharFieldIntegration(unittest.TestCase):

    def test_if_is_invalid_when_not_str_values(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField()

        serializer = StubStrictCharFieldSerializer(data={'name': 5})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, {
            'name': [serializers.ErrorDetail(string='Not a valid string.', code='invalid')]
        })

        serializer = StubStrictCharFieldSerializer(data={'name': True})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, {
            'name': [serializers.ErrorDetail(string='Not a valid string.', code='invalid')]
        })

    def test_none_value_is_valid(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField(required=False, allow_null=True)

        serializer = StubStrictCharFieldSerializer(data={'name': None})
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_is_valid(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField()

        serializer = StubStrictCharFieldSerializer(data={'name': 'some value'})
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)


class TestStrictBooleanFieldIntegration(unittest.TestCase):

    def test_if_is_invalid_when_not_boll_values(self):
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            is_active = StrictBooleanField()

        message_error = 'Must be a valid boolean.'
        serializer = StubStrictBooleanFieldSerializer(data={'is_active': 0})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, {
            'is_active': [
                serializers.ErrorDetail(string=message_error, code='invalid')
            ]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'is_active': 1})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, {
            'is_active': [
                serializers.ErrorDetail(string=message_error, code='invalid')
            ]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'is_active': 'True'})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, {
            'is_active': [
                serializers.ErrorDetail(string=message_error, code='invalid')
            ]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'is_active': 'False'})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, {
            'is_active': [
                serializers.ErrorDetail(string=message_error, code='invalid')
            ]
        })

    def test_is_valid(self):
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            is_active = StrictBooleanField(allow_null=True)

        serializer = StubStrictBooleanFieldSerializer(data={'is_active': None})
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        serializer = StubStrictBooleanFieldSerializer(data={'is_active': True})
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        serializer = StubStrictBooleanFieldSerializer(data={'is_active': False})
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
