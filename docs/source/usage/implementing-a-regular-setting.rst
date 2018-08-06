================
Regular settings
================

.. contents:: Contents:
    :local:
    :depth: 1


What is a regular setting?
==========================

Any setting that allows a user to override a simple Python type value is classed as a 'regular setting'. Cogweels doesn't limit the type of values you can use, but it's recommended that you stick to using well-known types, that are easy for your app's users to override.

When you request a value for a 'regular setting' from your app's settings module (e.g. ``yourapp.conf.settings``), it returns a pointer to the exact same value in memory (not a copy) e.g.:

If no override value is found, the default value you added to ``yourapp.conf.defaults.py`` is returned:

.. code-block:: python
    
    # yourapp/conf/defaults.py

    SETTING_NAME = 'default-value'

.. code-block:: console

    > from yourapp.conf import settings
    > from yourapp.conf import defaults

    > settings.SETTING_NAME
    'default-value'

    > settings.SETTING_NAME is defaults.SETTING_NAME
    True

If a user has added an override value to their Django settings (using the correct prefix and setting name), that exact value is returned:

.. code-block:: python
    
    # usersdjangoproject/settings/base.py

    YOURAPP_SETTING_NAME = 'override-value'

.. code-block:: console

    > from yourapp.conf import settings
    > from django.conf import settings as django_settings

    > settings.SETTING_NAME
    'override-value'

    > settings.SETTING_NAME is django_settings.YOURAPP_SETTING_NAME
    True


Some examples
-------------

You define app settings by simply adding variables to ``yourapp/conf/defaults.py`` with your preferred default values. e.g.:
    
.. code-block:: python

    # yourapp/conf/defaults.py

    # -------------------------
    # SIMPLE BINARY PREFERENCES
    # -------------------------

    SEND_EMAILS_ON_DISPATCH = True

    ADVANCED_ROUTING_ENABLED = True

    SHOW_PRODUCT_RECOMMENDATIONS_AT_CHECKOUT = False

    # ---------------------------------
    # LABELLING AND THEME CUSTOMISATION
    # ---------------------------------

    ADMIN_UI_PROJECT_NAME = "Project Name"

    HEADER_BACKGROUND_COLOUR = "#ca8ecc"

    AMAZING_WIDGET_THEME = "light"

    MAIN_MENU_MAX_DEPTH = 2

    # -----------------------
    # DEFAULT VALUE OVERRIDES
    # -----------------------

    DEFAULT_ARTICLE_PAGE_DEPTH = 3

    DEFAULT_HEADLINE_TEXT = "Spiderman - Friend or Foe?"

    # --------------------------
    # MORE COMPLEX CONFIGURATION
    # --------------------------

    DATA_CACHE_CONFIG = {
        'target_cache': "default",
        'timeout': 500,
        'cache_key_prefix': "__DATA__",
    }


Users will override these settings by adding override values to their Django settings, like so:

.. code-block:: python

    # usersdjangoproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    YOURAPP_ADMIN_UI_PROJECT_NAME = "The Best Project Ever!"

    YOURAPP_SEND_EMAILS_ON_DISPATCH = False

    YOURAPP_DATA_CACHE_CONFIG = {
        'target_cache': "yourapp",
        'timeout': 200,
        'cache_key_prefix': "__DATA__",
    }


Retrieving app setting values
=============================

Referencing a setting as a direct attribute of the setting helper or using the helper's ``get()`` method returns values **exactly** as they are defined in ``defaults.py``, or in your user's Django settings.

.. code-block:: console

    > from yourapp.conf import settings

    > settings.ADMIN_UI_PROJECT_NAME
    "The Best Project Ever!"

    > settings.get("ADMIN_UI_PROJECT_NAME")
    "The Best Project Ever!"

    > settings.SEND_EMAILS_ON_DISPATCH 
    False

    > settings.get("SEND_EMAILS_ON_DISPATCH") 
    False

    > settings.DATA_CACHE_CONFIG
    {'target_cache': "yourapp-data", 'timeout': None, 'cache_key_prefix': "__YOURAPPDATA__"}

    > settings.get("DATA_CACHE_CONFIG")
    {'target_cache': "yourapp-data", 'timeout': None, 'cache_key_prefix': "__YOURAPPDATA__"}

    > settings.DEFAULT_HEADLINE_TEXT
    "Spiderman - Friend or Foe?"

    > settings.get("DEFAULT_HEADLINE_TEXT")
    "Spiderman - Friend or Foe?"


Validation and error handling
=============================

Cogwheels doesn't apply any validation to regular setting values at all by default.

If you need to apply validation to setting values in your app, you'll need to implement this yourself. One way to do this would be to add a property method to your app's settings helper for the setting in question. e.g.:

.. code-block:: python
    
    # yourapp/conf/settings.py

    from cogwheels import OverrideValueFormatInvalid
    from yourapp.data.utils import is_cache_config_value_valid


    class TestAppSettingsHelper(BaseAppSettingsHelper):

        @property
        def DATA_CACHE_CONFIG(self):
            """
            Doing ``settings.DATA_CACHE_CONFIG`` will invoke this method
            instead of the default behavior, allowing us to apply custom
            validation to override values.
            """ 

            # The get() method's ``enforce_type`` argument can be used to ensure
            # values are of a specific type. It will also accept a tuple of types
            # if you're happy for the value to be one of several types.
            value = self.get('DATA_CACHE_CONFIG', enforce_type=dict)

            # If the value has been overridden, check it's validity
            if self.is_overridden('DATA_CACHE_CONFIG') and not is_cache_config_value_valid(value):
                raise OverrideValueFormatInvalid(
                    "The override value you've used for YOURAPP_DATA_CACHE_CONFIG is not valid."
                )

            # Don't forget to return the value!
            return value 


Behind the scenes
=================

When you request a regular setting value from ``settings`` using:

- ``settings.REGULAR_SETTING_NAME`` or
- ``settings.get('REGULAR_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a helpfully worded ``DeprecationWarning`` is raised to prompt users to review their implementation.
2.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_REGULAR_SETTING_NAME``), that value is returned.
3.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_REGULAR_SETTING_NAME``), and (after raising a helpfully worded ``DeprecationWarning``) returns that if found. 
4.  If no override value was found, the default value that you used in ``defaults.py`` is returned.

The setting value is also cached, so that steps 2-4 can be bypassed the next time the same setting value is requested.
