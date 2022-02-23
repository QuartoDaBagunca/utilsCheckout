from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("etl-py") \
    .getOrCreate()

def makeDFJDBC(conex:dict, table:str, pks:dict, makeTmpView:bool, type_format = None):

    # search DB credentials in AWS Secrets Manager

    url = conex.getUrl()
    user = conex.getUsr()
    password = conex.getPas()
    database = conex.getDb()
    driver = conex.getDve()
    query = "select {} tab.* from SAP_PRD.{} as tab"

    if (len(pks) == 0):
        primary_key = '1 as ID_stg, '
    elif (len(pks) == 1):
        primary_key = '({}) as ID_stg,'.format(pks[0])
    else:
        primary_key = '({}) as ID_stg,'.format(' || '.join(pks))

    hana_query = query.format(primary_key, table)

    print(hana_query)
    df = spark.read \
        .format("jdbc")  \
        .option("inferSchema", "true")  \
        .option("url", url) \
        .option("driver", driver)  \
        .option("database", database) \
        .option("query", hana_query) \
        .option("user", user) \
        .option("password", password) \
    .load()

    if makeTmpView:
        df.registerTempTable(table)

    return df