import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, regexp_replace, lower, count


def run(spark: SparkSession, input_path: str, output_path: str) -> None:
    logging.info("Reading text file from: %s", input_path)
    input_df = spark.read.text(input_path).toDF("line")
    new_wordcount_df = input_df.select(explode(split('line', ' ')).alias('line'))

    new_wordcount_df = new_wordcount_df.withColumn("line", regexp_replace(col('line'), "[,#''.;-]", ""))
    new_wordcount_df = new_wordcount_df.filter(col('line') != '').select(lower('line').alias('line'))
    count_of_words_df = new_wordcount_df.groupBy('line').agg(count('line').alias('word_count'))

    count_of_words_df.show(count_of_words_df.count())
        
    logging.info("Writing csv to directory: %s", output_path)
    df_pandas = count_of_words_df.toPandas()
    df_pandas.to_csv(os.path.join(output_path,'output.csv'),sep= '|', index=False)

    # try:
    #     input_df.coalesce(1).write.option("header","true").mode("overwrite").format("csv").save("output_path")
    #     count_of_words_df.write.format("csv").mode("overwrite").save(output_path+'/file.csv')
    # except Exception as e:
    #      print('Error due to : ',e)