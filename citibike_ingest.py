import logging

import sys
from pyspark.sql import SparkSession
from data_transformations.citibike import daily_driver

if __name__ == '__main__':
    LOG_FILENAME = 'project.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    logging.info(sys.argv)
    if len(sys.argv) is not 3:
        logging.warning("Input source and output path are required")
        sys.exit(1)

    spark = SparkSession.builder.appName("Citibike Pipeline: Ingest (daily_driver)").getOrCreate()
    sc = spark.sparkContext
    app_name = sc.appName
    logging.info("Application Initialized: " + app_name)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    daily_driver.run(spark, input_path, output_path)
    logging.info("Application Done: " + spark.sparkContext.appName)
    spark.stop()
