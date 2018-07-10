import warnings


class DeprecatedAppSetting:
    """
    An instance of ``DeprecatedAppSetting`` stores details about a deprecated
    app setting, and helps to raise warnings related with that deprecation.
    """
    def __init__(self, setting_name, renamed_to=None, replaced_by=None,
                 warning_category=None, guidance=None, message=None):
        self.setting_name = setting_name
        self.replacement_name = renamed_to or replaced_by
        self.is_renamed = renamed_to is not None
        self.warning_category = warning_category or DeprecationWarning
        self.guidance = guidance
        self.message = message
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

    def make_message(self, message_start, default_guidance=None):
        if self.message:
            return self.message
        if self.guidance is None and default_guidance:
            return message_start + ' ' + default_guidance
        if self.guidance:
            return message_start + ' ' + self.guidance
        return message_start

    def warn(self, message, **replacement_kwargs):
        warnings.warn(
            message.format(**replacement_kwargs),
            category=self.warning_category
        )

    def warn_if_referenced_directly(self):
        if self.replacement_name is not None:
            if self.is_renamed:
                msg = self.make_message(
                    "The {setting_name} app setting has been renamed to "
                    "{replacement_name}, and support for the {setting_name} "
                    "will be removed in {removed_in_version}.",
                    "Please update your code use {replacement_name}, or your "
                    "code may break once support is removed."
                )
            else:
                msg = self.make_message(
                    "The {setting_name} app setting is deprecated in favour "
                    "of using {replacement_name}, and support for "
                    "{setting_name} will be removed in {removed_in_version}.",
                    "Please update your code use {replacement_name}, or your "
                    "code may break once support is removed. There are some "
                    "functional differences between the two settings, so "
                    "please review the release notes for more information."
                )
        else:
            msg = self.make_message(
                "The {setting_name} app setting is deprecated, and will be "
                "removed in {removed_in_version}.",
                "Please remove references to {setting_name} from your code to "
                "avoid code breakages once support is removed."
            )

        self.warn(
            msg,
            setting_name=self.setting_name,
            replacement_name=self.replacement_name,
            removed_in_version=self.get_removed_in_version_text()
        )

    def warn_if_deprecated_value_used_by_replacement(self):
        if self.is_renamed:
            msg = self.make_message(
                "The {setting_name} setting has been renamed to "
                "{replacement_name}, and support for {setting_name} will be "
                "removed in {removed_in_version}.",
                "To preserve the current behavior, please update your Django "
                "settings to use {replacement_name} instead."
            )
        else:
            msg = self.make_message(
                "The {setting_name} setting is deprecated in favour of using "
                "{replacement_name}, and support for {setting_name} will be "
                "removed in {removed_in_version}.",
                "To preserve the current behavior, please update your Django "
                "settings to use {replacement_name} instead. There are some "
                "functional differences between the two settings, so "
                "please review the release notes for more information."
            )
        self.warn(
            msg,
            setting_name=self.prefix + self.setting_name,
            replacement_name=self.prefix + self.replacement_name,
            removed_in_version=self.get_removed_in_version_text()
        )
