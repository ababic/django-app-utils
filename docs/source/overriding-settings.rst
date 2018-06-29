=======================
Overriding app settings
=======================

Once you have configured Cogwheels for your app and packaged the changes into a new release, users of your app should be able override any of the default values by adding alternative values to their project's Django settings module. For example: 

.. code-block:: python

    # userproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    YOURAPP_MAX_ITEMS_PER_ORDER = 2
    YOURAPP_ORDER_ITEM_MODEL = 'userproject_orders.CustomOrderItem'
    YOURAPP_DISCOUNTS_BACKEND = 'userproject.discounts.custom_discount_backend'
    YOURAPP_ORDER_FORM_CLASS = 'userproject.orders.forms.CustomOrderForm'


Automatic setting namespacing
=============================

I'm sure you noticed that that the above variable names are all prefixed with `YOURAPP_``. This prefix will differ for your app, depending on the package name. 

This namespacing of settings is important, as not only does it help users of your app to remember which app their settings apply to, but it also helps to prevent setting name clashes between apps.


Finding out the prefix for your app
-----------------------------------

You can find out what the prefix is for your app by calling the setting's modules ``get_prefix()`` method, like so:
    
.. code-block:: console

    >>> from yourproject.conf import settings
    >>> settings.get_prefix()
    'YOURPROJECT_'


Changing the prefix for your app
--------------------------------

You can change this prefix to whatever you like by setting a ``prefix`` attribute on your settings helper class. For example, this:

.. code-block:: python

    # yourapp/conf/settings.py
    
    class MyAppSettingsHelper(BaseAppSettingsHelper):
        prefix = 'CUSTOM'  # No need for a trailing underscore here

Would result in this:

.. code-block:: console

    >>> from yourproject.conf import settings
    >>> settings.get_prefix()
    'CUSTOM_'


Documenting your settings
=========================

In order for users to know what they can override (and how), you'll need to document the settings somewhere.

If you don't have one already, I would highly recommend adding a 'Settings reference' page to your documentation, similar to the one in the one in the `wagtailmenus documentation
<https://wagtailmenus.readthedocs.io/en/latest/settings_reference.html>`_.

You should clearly explain what each setting does, what type of value is expected, and any relevant limitations that apply to the value (such as upper/lower boundaries for numbers, or maximum lengths for strings).

