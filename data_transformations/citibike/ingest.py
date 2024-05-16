import logging
from typing import List
import data_transformations.citibike.distance_transformer as bike_distance
from pyspark.sql import SparkSession


def sanitize_columns(columns: List[str]) -> List[str]:
    return [column.replace(" ", "_") for column in columns]


def run(spark, ingestPath, transformationPath):
    df = spark.read.parquet(ingestPath)
    df.show()
    df = bike_distance.computeDistances(spark, df)
    df.show()
    df.write.parquet(transformationPath,mode='append')
