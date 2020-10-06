import logging

import sys
from pyspark.sql import SparkSession

from data_transformations.wordcount import word_count_transformer

LOG_FILENAME = 'project.log'
APP_NAME = "WordCount"

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    logging.info(sys.argv)

    if len(sys.argv) is not 3:
        logging.warning("Input .txt file and output path are required")
        sys.exit(1)

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    sc = spark.sparkContext
    app_name = sc.appName
    logging.info("Application Initialized: " + app_name)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    word_count_transformer.run(spark, input_path, output_path)
    logging.info("Application Done: " + spark.sparkContext.appName)
    spark.stop()
