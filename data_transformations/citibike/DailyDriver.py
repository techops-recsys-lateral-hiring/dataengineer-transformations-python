import sys
import logging
from pyspark.sql import SparkSession


def run(spark, ingest_path, transformation_path):
    logging.info("Reading text file from: " + ingest_path)

    input_df = spark.read.format("org.apache.spark.csv").option("header", True).csv(ingest_path)

    columns = input_df.columns
    renamed_columns = [column.replace(" ", "_") for column in columns]
    ref_df = input_df.toDF(*renamed_columns)
    ref_df.printSchema()

    ref_df.write.parquet(transformation_path)
