from pyspark.sql import SparkSession

SPARK = SparkSession.builder.appName("IntegrationTests").getOrCreate()
