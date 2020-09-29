from pyspark.sql import SparkSession

SPARK = SparkSession.builder.appName("CitibikeTransformerTest").getOrCreate()
