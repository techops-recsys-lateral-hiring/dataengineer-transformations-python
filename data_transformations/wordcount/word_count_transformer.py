import logging

from pyspark.sql import SparkSession


def run(spark: SparkSession, input_path: str, output_path: str) -> None:
    logging.info("Reading text file from: %s", input_path)
    input_df = spark.read.text(input_path)

    logging.info("Writing csv to directory: %s", output_path)

    input_df.coalesce(1).write.csv(output_path, header=True)
