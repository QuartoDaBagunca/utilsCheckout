from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import urllib.request, time
import boto3
import json

aws_secrets = boto3.client("secretsmanager", region_name = "us-east-1")
hana_secrets = json.loads(aws_secrets.get_secret_value(SecretId="HANA-connection")['SecretString'])

spark = SparkSession.builder.appName("etl-yelp-py") \
    .getOrCreate()

class PipelinesMonitoring():

    def __init__(self):

        self.BUCKET_NAME = "a3data-548080336967"
        self.nome_tabela_s3 = "QUERY_ATHENA"
        self.nome_tabela_jdbc = "QUERY_HANA"
        
        jdbc_secrets = hana_secrets

        self.url = jdbc_secrets["url"]
        self.user = jdbc_secrets["user"]
        self.password = jdbc_secrets["password"]
        self.database = jdbc_secrets["database"]
        self.driver = jdbc_secrets["driver"]

    def query_df_s3(self, query:str, table:str) -> DataFrame:

        bucket = f"s3a://{self.BUCKET_NAME}/consumer-zone/{table}"
        
        view_name = table.replace('-', '_')

        df_table = spark.read \
            .format("delta") \
            .load(bucket)

        df_table.createOrReplaceTempView(view_name)
        
        df = spark.sql(query)

        return df

    def query_df_jdbc(self, query:str) -> DataFrame:

        df = (
            spark.read.format("jdbc")
            .option("inferSchema", "true")
            .option("driver", self.driver)
            .option("user", self.user)
            .option("password", self.password)
            .option("database", self.database)
            .option("url", self.url)
            .option("query", query)
            .load()
        )

        return df
    
    def is_equals(self, df1:DataFrame, df2:DataFrame) -> DataFrame:
        
        df1.createOrReplaceTempView(self.nome_tabela_s3)

        df2.createOrReplaceTempView(self.nome_tabela_jdbc)
        
        query_validacao = """
            select * from {}
                EXCEPT
            select * from {}
        """

        result = spark.sql(query_validacao.format(self.nome_tabela_jdbc, self.nome_tabela_s3))
        
        return result