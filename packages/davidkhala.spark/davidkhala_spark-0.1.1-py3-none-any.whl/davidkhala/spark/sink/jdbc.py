from enum import Enum

from pyspark.sql.connect.dataframe import DataFrame

from davidkhala.spark.sink import Write


class SQLServer(Write):
    class Mode(Enum):
        append = "append"
        overwrite = "overwrite"

    def __init__(self, df: DataFrame, *,
                 server: str, database: str, table: str, user: str, password: str,
                 mode: Mode = Mode.append
                 ):
        super().__init__(df)
        self.url = f"jdbc:sqlserver://{server};databaseName={database}"
        self.table = table
        self.mode = mode.value
        self.properties = {
            "user": user,
            "password": password,
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }

    def start(self):
        self.batch.jdbc(
            self.url, self.table, self.mode, self.properties
        )
