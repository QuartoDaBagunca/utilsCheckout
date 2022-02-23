# import libraries

from os.path import abspath
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os

# set default location for warehouse

warehouse_location = abspath('spark-warehouse')

def getSpark(type_session:str, extra_jars:str = None) -> SparkSession:
    
    # init session

    spark = None
    if type_session == "PIF":
        spark = SparkSession \
                .builder \
                .appName("etl-py") \
                .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0") \
                .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                .config(
                    "spark.sql.catalog.spark_catalog",
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog",
                ) \
                .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
                .config("spark.jars", extra_jars) \
                .config("spark.sql.warehouse.dir", warehouse_location) \
                .getOrCreate()
    elif type_session == "DELTA":
        spark = SparkSession \
                .builder \
                .appName("etl-py") \
                .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0") \
                .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                .config(
                    "spark.sql.catalog.spark_catalog",
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog",
                ) \
                .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
                .config("spark.sql.warehouse.dir", warehouse_location) \
                .getOrCreate()
    else:
        spark = SparkSession \
                .builder \
                .appName("etl-py") \
                .config("spark.sql.warehouse.dir", warehouse_location) \
                .getOrCreate()

    spark.sparkContext \
        ._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.environ['AWS_ACCESS_KEY_ID'])

    spark.sparkContext \
        ._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.environ['AWS_SECRET_ACCESS_KEY'])

    spark.sparkContext \
        ._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.amazonaws.com")

    return spark