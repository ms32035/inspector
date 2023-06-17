from .sql_connector import SQLConnector


class RedshiftConnector(SQLConnector):
    sqla_connection_string_template = "redshift+psycopg2://{login}:{password}@{host}:{port}/{db}"
