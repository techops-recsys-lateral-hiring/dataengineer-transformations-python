import logging

import sys
from pyspark.sql import SparkSession

from data_transformations.citibike import distance_transformer

LOG_FILENAME = 'project.log'
APP_NAME = "Citibike Pipeline: Distance Calculation"

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    arguments = sys.argv

    if len(arguments) is not 3:
        logging.warning("Dataset file path and output path not specified!")
        sys.exit(1)

    dataset_path = arguments[2]
    output_path = arguments[3]

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    logging.info("Application Initialized: " + spark.sparkContext.appName)
    distance_transformer.run(spark, dataset_path, output_path)
    logging.info("Application Done: " + spark.sparkContext.appName)

    spark.stop()
