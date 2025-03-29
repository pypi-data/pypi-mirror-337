from os.path import exists, join
from .config import datalake, warehouse
from .tools.db import get_db_url
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


def create_datalake(file_name: str = "arquee.txt"):
    origin = get_db_url("ORIGIN_DB")

    if not exists(datalake):
        raise FileNotFoundError("Folder datalake not found, run command Arquee")

    if exists(file_name):
        spark = get_spark_session()
        with open(file_name, "r") as file:
            tables = set(table.upper().strip() for table in file.readlines())

        for table in tables:
            destiny_path = join(datalake, table)
            df: DataFrame = spark.read.jdbc(origin, table)
            df.write.parquet(destiny_path)


spark = None


def get_spark_session() -> SparkSession:
    global spark
    if not spark:
        spark = (
            SparkSession.builder.appName("ETL")
            .master("local[*]")
            .config("spark.executor.memory", "4g")
            .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")
    return spark


def get_dataframe(table_name: str):
    spark: SparkSession = get_spark_session()
    folder_path = join(datalake, table_name.upper().strip())
    df: DataFrame = spark.read.parquet(folder_path)
    return df


def save_dataframe(df: DataFrame, table_name: str):
    folder_path = join(warehouse, table_name.upper().strip())
    df.write.parquet(folder_path, "overwrite")
