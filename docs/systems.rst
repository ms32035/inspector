Systems, Environments, Instances
================================

This page explains the basic concepts in the Systems module

System
------

An abstract application that has a database
and where you will run your checks.

Examples:

* CRM
* Some backend app
* Data warehouse

A system does not have any connection details or credentials.

Environment
-----------

A logical grouping of system instances/deployments environment, such as:

* Dev
* QA
* Staging
* Production

Instance
--------

A single deployment of a system in an environment,
including connection details and credentials.
