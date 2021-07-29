import logging
from typing import List

from pyspark.sql import SparkSession


def sanitize_columns(columns: List[str]) -> List[str]:
    return [column.replace(" ", "_") for column in columns]


def run(spark: SparkSession, ingest_path: str, transformation_path: str) -> None:
    logging.info("Reading text file from: %s", ingest_path)
    input_df = spark.read.format("org.apache.spark.csv").option("header", True).csv(ingest_path)
    renamed_columns = sanitize_columns(input_df.columns)
    ref_df = input_df.toDF(*renamed_columns)
    ref_df.printSchema()
    ref_df.show()

    ref_df.write.parquet(transformation_path)
