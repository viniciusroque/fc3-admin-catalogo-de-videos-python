from dataclasses import fields
import unittest
from unittest.mock import MagicMock, PropertyMock, patch
from rest_framework import serializers

from __seedwork.domain.exceptions import ValidationException
from __seedwork.domain.validators import DRFValidator, ValidatorFieldsInterface, ValidatorRules


class TestValidatorRules(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values('some value', 'prop') #NOSONAR
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'some value')
        self.assertEqual(validator.prop, 'prop')

    def test_required_rule(self):

        invalid_values = [None, '']
        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').required()

            self.assertEqual(assert_error.exception.args[0], 'The prop is required') #NOSONAR

        valid_values = [
            'some value',
            0,
            5,
            False
        ]
        for valid_value in valid_values:
            validator = ValidatorRules.values(valid_value, 'prop')
            self.assertIsInstance(validator.required(), ValidatorRules)

    def test_string_rule(self):
        invalid_values = [
            5,
            True,
            {}
        ]

        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').string()

            self.assertEqual(assert_error.exception.args[0], 'The prop must be a string')


        valid_values = [
            'some value',
            '',
            None
        ]
        for valid_value in valid_values:
            validator = ValidatorRules.values(valid_value, 'prop')
            self.assertIsInstance(validator.string(), ValidatorRules)

    def test_max_length_rule(self):
        invalid_values = [
            't' * 5
        ]

        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').max_length(4)

            self.assertEqual(
                assert_error.exception.args[0],
                'The prop must be less than 4 characters'
            )

        valid_values = [
            't' * 5,
            '',
            None
        ]
        for valid_value in valid_values:
            validator = ValidatorRules.values(valid_value, 'prop')
            self.assertIsInstance(validator.max_length(5), ValidatorRules)


    def test_boolean_rule(self):
        invalid_values = [
            'True',
            5,
            'False',
            'true',
            'false',
            {},
            ''
        ]

        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').boolean()

            self.assertEqual(assert_error.exception.args[0], 'The prop must be a boolean')

        valid_values = [
            None,
            True,
            False
        ]
        for valid_value in valid_values:
            validator = ValidatorRules.values(valid_value, 'prop')
            self.assertIsInstance(validator.boolean(), ValidatorRules)

    def test_throw_a_validation_exception_when_combine_more_than_on_rules(self):
        invalid_values = [
            None,
            ''
        ]

        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').required().string().max_length(5)

            self.assertEqual(assert_error.exception.args[0], 'The prop is required')


        invalid_values = [
            5,
            {}
        ]
        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').required().string().max_length(5)

            self.assertEqual(assert_error.exception.args[0], 'The prop must be a string')


        invalid_values = [
            't' * 5
        ]
        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').required().string().max_length(4)

            self.assertEqual(
                assert_error.exception.args[0],
                'The prop must be less than 4 characters'
            )

        invalid_values = [
            None,
            ''
        ]
        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').required().boolean()

            self.assertEqual(assert_error.exception.args[0], 'The prop is required')

        invalid_values = [
            5,
            {}
        ]
        for invalid_value in invalid_values:
            msg = f'value: {invalid_value}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(invalid_value, 'prop').required().boolean()

            self.assertEqual(assert_error.exception.args[0], 'The prop must be a boolean')


    def test_valid_cases_for_combination_between_rules(self):
        ValidatorRules.values('test', 'prop').required().string()
        ValidatorRules.values('t' * 5, 'prop').required().string().max_length(5)

        ValidatorRules.values(True, 'prop').required().boolean()
        ValidatorRules.values(False, 'prop').required().boolean()

        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True) #NOSONAR


class TestValidatorFieldsInterface(unittest.TestCase):

    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()

        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class ValidatorFieldsInterface " +
            "with abstract method validate"
        )

    def test_fields(self):
        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_class[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)

class TestDRFValidatorUnit(unittest.TestCase):

    @patch.object(serializers.Serializer, 'is_valid', return_value=True)
    @patch.object(
        serializers.Serializer,
        'validated_data',
        return_value={'field': ['value']},
        new_callable=PropertyMock
    )
    def test_if_validated_data_is_set(
        self,
        mock_validated_data: PropertyMock,
        mock_is_valid: MagicMock,
    ):
        validator = DRFValidator()
        is_valid = validator.validate(serializers.Serializer())
        self.assertTrue(is_valid)
        mock_is_valid.assert_called_once()
        mock_validated_data.assert_called()

        self.assertEqual(validator.validated_data, {'field': ['value']})

    @patch.object(serializers.Serializer, 'is_valid', return_value=False)
    @patch.object(
        serializers.Serializer,
        'errors',
        return_value={'field': ['some error']},
        new_callable=PropertyMock
    )
    def test_if_errors_is_set(
        self,
        mock_errors: PropertyMock,
        mock_is_valid: MagicMock,
    ):
        validator = DRFValidator()
        is_valid = validator.validate(serializers.Serializer())
        self.assertFalse(is_valid)
        mock_is_valid.assert_called_once()
        mock_errors.assert_called()

        self.assertEqual(validator.errors, {'field': ['some error']})
