import logging

import sys
from pyspark.sql import SparkSession

from data_transformations.citibike import ingest

LOG_FILENAME = 'project.log'
APP_NAME = "Citibike Pipeline: Ingest"

def main(args):

    if len(args) < 4:
        logging.warning("Input source and output path are required")
        sys.exit(1)
    else:
        input_path = args[2]
        output_path = args[3]

    spark = SparkSession.builder.appName("Citibike Transformer").getOrCreate()
    logging.info("Application Initialized: " + spark.sparkContext.appName)
    ingest.run(spark, input_path, output_path)
    logging.info("Application Done: " + spark.sparkContext.appName)

    spark.stop()