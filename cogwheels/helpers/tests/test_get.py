from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from cogwheels import DefaultValueTypeInvalid
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.conf import defaults


class TestGetValueMethod(AppSettingTestCase):

    def test_raises_error_if_no_default_defined(self):
        with self.assertRaises(ImproperlyConfigured):
            self.appsettingshelper.get('NOT_REAL_SETTING')

    def test_integer_setting_returns_default_value_by_default(self):
        self.assertEqual(
            self.appsettingshelper.get('INTEGER_SETTING'),
            defaults.INTEGER_SETTING
        )

    @override_settings(COGWHEELS_TESTS_INTEGER_SETTING=1234)
    def test_integer_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('INTEGER_SETTING')
        self.assertNotEqual(result, defaults.INTEGER_SETTING)
        self.assertEqual(result, 1234)

    def test_str_type_enforcement_raises_error(self):
        with self.assertRaises(DefaultValueTypeInvalid):
            self.appsettingshelper.get('INTEGER_SETTING', enforce_type=str)

    def test_multiple_type_enforcement_raises_error(self):
        with self.assertRaises(DefaultValueTypeInvalid):
            self.appsettingshelper.get('INTEGER_SETTING', enforce_type=(str, list, float))

    def test_multiple_type_enforcement_does_not_raise_error_if_one_type_matches(self):
        self.appsettingshelper.get('INTEGER_SETTING', enforce_type=(str, list, int))

    def test_boolean_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get('BOOLEAN_SETTING'),
            defaults.BOOLEAN_SETTING
        )

    @override_settings(COGWHEELS_TESTS_BOOLEAN_SETTING=True)
    def test_boolean_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('BOOLEAN_SETTING')
        self.assertNotEqual(result, defaults.BOOLEAN_SETTING)
        self.assertIs(result, True)

    def test_string_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get('STRING_SETTING'),
            defaults.STRING_SETTING
        )

    @override_settings(COGWHEELS_TESTS_STRING_SETTING='abc')
    def test_string_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('STRING_SETTING')
        self.assertNotEqual(result, defaults.STRING_SETTING)
        self.assertIs(result, 'abc')

    def test_tuples_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get('TUPLES_SETTING'),
            defaults.TUPLES_SETTING
        )

    @override_settings(COGWHEELS_TESTS_TUPLES_SETTING=())
    def test_tuples_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('TUPLES_SETTING')
        self.assertNotEqual(result, defaults.TUPLES_SETTING)
        self.assertIs(result, ())
