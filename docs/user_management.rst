User management
===============

Users and authentication
------------------------

Authentication is done with django-allauth (https://django-allauth.readthedocs.io/en/latest/)
Please refer to that documentation for all configuration details.

Django Admin
------------

To create a Django superuser with full admin panel access,
execute the standard command

.. code-block:: bash

    python manage.py createsuperuser


Default groups
--------------

There are some default groups that you might want to use
(https://github.com/ms32035/inspector/blob/master/inspector/base/management/commands/default_auth_groups.py)

To enable these, run the following command:

.. code-block:: bash

    python manage.py default_auth_groups


Assigning permissions
--------------

Assign users to groups in Django Admin
