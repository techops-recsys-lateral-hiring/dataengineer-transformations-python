import logging
import thoughtworks.wordcount.utils as wordcount_utils
from pyspark.sql import SparkSession

def run(spark, inputPath, outputPath):

    logging.info("Reading text file from: " + inputPath)

    input_df = spark.read.text(inputPath)
    split_df = wordcount_utils.splitWords(spark, input_df)
    count_df = wordcount_utils.countByWord(spark, split_df)

    logging.info("Writing csv to directory: " + outputPath)

    count_df.show
    count_df.coalesce(1).write.csv(outputPath,mode='append')