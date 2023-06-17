API
===

Inspector is built around REST APIs with Django Rest Framework.

In development configuration, standard Swagger UI is available
at :code:`/` for authenticated users.

Authentication for all APIs can be done through:
* a JWT token
* API token obtained from the user profile

Additionally, the development configuration allows for session
based authentication.
