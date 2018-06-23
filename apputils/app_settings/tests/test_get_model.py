from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from apputils.tests.base import AppSettingTestCase
from apputils.tests.models import DefaultModel, ReplacementModel


class TestValidModelSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``TEST_VALID_MODEL``
    """
    def test_returns_default_model_by_default(self):
        self.assertEqual(
            self.appsettingshelper.get_model('VALID_MODEL'), DefaultModel,
        )

    @override_settings(TEST_VALID_MODEL='tests.ReplacementModel')
    def test_successful_override(self):
        self.assertEqual(
            self.appsettingshelper.get_model('VALID_MODEL'), ReplacementModel
        )

    @override_settings(TEST_VALID_MODEL='no_dots_here')
    def test_raises_error_when_format_is_invalid(self):
        message_expected = (
            "Your TEST_VALID_MODEL setting value is invalid. Model strings "
            "must be in the format 'app_label.Model', which 'no_dots_here' "
            "does not adhere to."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_model('VALID_MODEL')

    @override_settings(TEST_VALID_MODEL='tests.NonExistentModel')
    def test_raises_error_when_model_not_installed(self):
        message_expected = (
            "Your TEST_VALID_MODEL setting value is invalid. The model "
            "'tests.NonExistentModel' does not appear to be installed."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_model('VALID_MODEL')


class TestInvalidDefaultModelSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    'model import string') is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_error_when_format_is_invalid(self):
        message_expected = (
            "The default value defined for the INCORRECT_FORMAT_MODEL app "
            "setting is invalid. Model strings must be in the format "
            "'app_label.Model', which 'apputils.tests.DefaultModel' does not "
            "adhere to."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_model('INCORRECT_FORMAT_MODEL')

    def test_raises_error_when_model_not_installed(self):
        message_expected = (
            "The default value defined for the UNAVAILABLE_MODEL app setting "
            "is invalid. The model 'apputils.UnavailableModel' does not "
            "appear to be installed."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_model('UNAVAILABLE_MODEL')
