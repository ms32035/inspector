Installation
============

Inspector is a Django app with a Celery worker for executing the checks.
If you know Django, and how to deploy Django apps, you are already one step ahead.

Docker images
-------------

Docker is the only supported way of deploying Inspector.
The base Docker Image :code:`ms32035/inspector` contains only PostgreSQL database drivers.
See :ref:`Extending` to learn how to add your own drivers


Develop
~~~~~~~

The :code:`develop` image contains only dependencies required to run the app in development mode,
with code being mounted from the current directory. It is the fastest way to get you started,
but under no circumstances this should be used to run in production.

Steps to get you up and running:

1) Clone the repo
2) :code:`docker-compose -f docker-compose-develop.yml up`

This will also deploy Redis and Postgres.
The environment will be running off the configuration in:

* :code:`.envs/.develop/.inspector`
* :code:`.envs/.develop/.postgres`
* :code:`config/settings/local.py`

Django's development server will be listening on port :code:`8000`.

Main
~~~~

The image tagged :code:`master` contains the app code from the master branch.

Steps for easy deployment:

    * :code: `docker-compose up`

This will also deploy Redis and Postgres. The environment will be running off the configuration in:

* :code:`.envs/.production/.inspector`
* :code:`.envs/.production/.postgres`
* :code:`config/settings/production.py`

This will start an HTTP on port :code:`5000`.
It's highly recommended that you use a HTTPS proxy in front such as NGINX.

Helm chart
~~~~~~~~~~

Official Inspector Helm chart can be found here:

* https://github.com/ms32035/inspector-helm

Extending
~~~~~~~~~

Each Inspector deployment will need a separate set of database drivers.
Python packages for various databases can be found in
:code:`inspector/requirements/option-<rdbms_name>.txt` files,
and you need to build your own Docker image,
for example like this:

.. code-block:: bash

    FROM ms32035/inspector:master
    USER root
    RUN pip install --no-cache-dir -r /requirements/option-mysql.txt
    USER django
