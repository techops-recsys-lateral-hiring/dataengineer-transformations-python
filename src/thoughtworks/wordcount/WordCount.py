import logging
import thoughtworks.wordcount.utils as wordcount_utils


def run(spark, input_path, output_path):
    logging.info("Reading text file from: " + input_path)

    input_df = spark.read.text(input_path)
    split_df = wordcount_utils.split_words(spark, input_df)
    count_df = wordcount_utils.count_by_word(spark, split_df)

    logging.info("Writing csv to directory: " + output_path)

    count_df.show()
    count_df.coalesce(1).write.csv(output_path, mode='append')
