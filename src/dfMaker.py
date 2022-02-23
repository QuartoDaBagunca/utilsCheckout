from src.utils import dfByStorage
from src.utils import dfByJDBC
# from src.utils import dfWriter
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("etl-py") \
    .getOrCreate()

def simple_temp_views(bucket:str, table_names:dict, query:str, conex:bool = None):

    for table, param in table_names.items():
        if conex:
            dfByJDBC.makeDFJDBC(None, table, param.get("pk"), True)
        else:
            dfByStorage.makeDFStorage(bucket, table, True, query.format(table))

def simple_df_write(bucket:str, bucket_destino:str, table_names:dict, type_target_format:str,  query:str, conex:bool = None):

    for table, param in table_names.items():
        if conex:
            df = dfByJDBC.makeDFJDBC(None, table, param.get("pk"), False)

            dfWriter.makeDataset(df, bucket_destino, table, type_target_format)
        else:
            df = dfByStorage.makeDFStorage(bucket, table, True, query.format(table))
            
            dfWriter.makeDataset(df, bucket_destino, table, type_target_format)