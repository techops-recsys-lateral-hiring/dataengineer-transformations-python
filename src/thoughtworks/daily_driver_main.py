import sys
import logging
from pyspark.sql import SparkSession

import thoughtworks.citibike.DailyDriver as DailyDriver


def main(args):
    if len(args) < 4:
        logging.warning("Input source and output path are required")
        sys.exit(1)
    else:
        spark = SparkSession.builder.appName("Skinny Pipeline: Ingest").getOrCreate()
        logging.info("Application Initialized: " + spark.sparkContext.appName)
        input_path = args[2]
        output_path = args[3]

    DailyDriver.run(spark, input_path, output_path)
    logging.info("Application Done: " + spark.sparkContext.appName)

    spark.stop()
