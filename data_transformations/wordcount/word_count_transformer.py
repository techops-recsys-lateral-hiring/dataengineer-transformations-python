import logging


def run(spark, input_path, output_path):
    logging.info("Reading text file from: " + input_path)
    input_df = spark.read.text(input_path)

    logging.info("Writing csv to directory: " + output_path)
    input_df.coalesce(1).write.csv(output_path)
