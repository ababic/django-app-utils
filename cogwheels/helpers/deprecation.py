import warnings


class DeprecatedAppSetting:
    """
    An instance of ``DeprecatedAppSetting`` stores details about a deprecated
    app setting, and helps to raise warnings related with that deprecation.
    """
    def __init__(
        self, setting_name, renamed_to=None, replaced_by=None,
        warning_category=None, additional_guidance=None
    ):
        self.setting_name = setting_name
        self.replacement_name = renamed_to or replaced_by
        self.is_renamed = renamed_to is not None
        self.warning_category = warning_category or DeprecationWarning
        self.additional_guidance = additional_guidance
        self._prefix = ''
        self.is_imminent = not issubclass(
            self.warning_category, PendingDeprecationWarning)

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    def get_removed_in_version_text(self):
        if self.is_imminent:
            return 'the next version'
        return 'two versions time'

    def _raise_warning(self, message, **replacement_kwargs):
        if self.additional_guidance:
            message += ' ' + self.additional_guidance
        warnings.warn(
            message.format(
                prefix=self.prefix,
                setting_name=self.setting_name,
                replacement_name=self.replacement_name,
                removed_in_version=self.get_removed_in_version_text()
            ),
            category=self.warning_category
        )

    def warn_if_setting_attribute_referenced(self):
        if self.replacement_name is not None:
            if self.is_renamed:
                self._raise_warning(
                    "The '{setting_name}' settings helper attribute has been renamed to "
                    "'{replacement_name}'. Please update your code to reference "
                    "'settings.{replacement_name}' instead, as continuing to reference "
                    "'settings.{setting_name}' will raise an AttributeError after support is "
                    "removed in {removed_in_version}."
                )
                return
            self._raise_warning(
                "The '{setting_name}' settings helper attribute is deprecated in favour of using "
                "'{replacement_name}'. Please update your code to reference "
                "'settings.{replacement_name}' instead, as continuing to reference "
                "'settings.{setting_name}' will raise an AttributeError after support is removed in "
                "{removed_in_version}."
            )
            return
        self._raise_warning(
            "The '{setting_name}' settings helper attribute is deprecated. Please remove any "
            "references to 'settings.{setting_name}' from your project, as this will raise an "
            "AttributeError after support is removed in {removed_in_version}."
        )

    def warn_if_user_using_old_setting_name(self):
        if self.is_renamed:
            self._raise_warning(
                "The '{prefix}{setting_name}' setting has been renamed to "
                "'{prefix}{replacement_name}'. Please update your Django settings to use the new "
                "setting name, otherwise the app will resort to default behaviour once support for "
                "the old setting is removed in {removed_in_version}.",
            )
            return
        self._raise_warning(
            "The '{prefix}{setting_name}' setting is deprecated in favour of using "
            "'{prefix}{replacement_name}'. Please update your Django settings to use the new "
            "setting, otherwise the app will resort to default behaviour once support for the old "
            "setting is removed in {removed_in_version}.",
        )
