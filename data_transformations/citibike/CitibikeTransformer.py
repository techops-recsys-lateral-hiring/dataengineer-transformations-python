import sys
import logging
import data_transformations.citibike.utils as citibike_utils
from pyspark.sql import SparkSession


def run(spark, ingestPath, transformationPath):
    df = spark.read.parquet(ingestPath)
    df.show()
    df = citibike_utils.compute_distance(spark, df)
    df.show()
    df.write.parquet(transformationPath,mode='append')
