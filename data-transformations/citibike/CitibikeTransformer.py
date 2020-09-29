import sys
import logging
import thoughtworks.citibike.utils as citibike_utils
from pyspark.sql import SparkSession


def run(spark, ingestPath, transformationPath):
    df = spark.read.parquet(ingestPath)
    df.show()
    df = citibike_utils.computeDistances(spark, df)
    df.show()
    df.write.parquet(transformationPath,mode='append')