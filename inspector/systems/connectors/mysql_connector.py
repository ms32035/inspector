from .sql_connector import SQLConnector


class MysqlConnector(SQLConnector):
    sqla_connection_string_template = "mysql://{login}:{password}@{host}:{port}/{db}"
