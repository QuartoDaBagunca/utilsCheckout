from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from delta.tables import *

spark = SparkSession \
    .builder \
    .appName("etl-py") \
.getOrCreate()

def makeDataset(df:DataFrame, bucket_destino:str, table:str, type_target_format:str, partition_column:str = None):

    if partition_column == None:
        df.coalesce(5).write \
            .format(type_target_format) \
            .option("mergeSchema", "true") \
            .mode("overwrite") \
            .save(bucket_destino.format(table))
    else:
        df.coalesce(1).write \
            .format(type_target_format) \
            .option("mergeSchema", "true") \
            .mode("overwrite") \
            .partitionBy(partition_column) \
        .save(bucket_destino.format(table))

    if type_target_format == "delta":
        staging_zone = DeltaTable.forPath(spark, bucket_destino.format(table))
        staging_zone.vacuum(0)

        # generate manifest to connect to Athena
        staging_zone.generate("symlink_format_manifest")