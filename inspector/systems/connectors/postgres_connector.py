from .sql_connector import SQLConnector


class PostgresConnector(SQLConnector):
    sqla_connection_string_template = "postgresql+psycopg://{login}:{password}@{host}:{port}/{db}"
    jdbc_connection_string_template = "jdbc:postgresql://{host}:{port}/{db}"
    default_port = 5432
    jdbc_driver_class = "org.postgresql.Driver"
    jar_package = "org.postgresql:postgresql:42.6.0"
