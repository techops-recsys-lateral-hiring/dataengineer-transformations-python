import datetime
import logging
import os

from pyspark.sql import SparkSession

import data_transformations.wordcount.WordCount as WordCount


def main(args):
    spark = SparkSession.builder.appName("Word Count").getOrCreate()
    logging.info("Application Initialized: " + spark.sparkContext.appName)

    if len(args) < 4:
        base_path = os.getcwd()
        input_path = base_path + "/test/wordcount/data/words.txt"
        output_path = base_path + "/test/wordcount/test-" + str(datetime.datetime.now())
    else:
        input_path = args[2]
        output_path = args[3]

    WordCount.run(spark, input_path, output_path)
    logging.info("Application Done: " + spark.sparkContext.appName)

    spark.stop()
