from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("etl-py") \
    .getOrCreate()

def makeDFStorage(bucket:str, table:str, makeTmpView:bool, query:str = None, type_format:str = "parquet"):

    df = spark.read \
        .format(type_format) \
        .load(bucket.format(table))

    if makeTmpView:
        df.registerTempTable(table)

    if (query != None):
        df = spark.sql(query)

    return df