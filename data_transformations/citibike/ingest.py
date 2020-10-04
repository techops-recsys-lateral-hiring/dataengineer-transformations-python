import logging


def sanitize_columns(columns):
    return [column.replace(" ", "_") for column in columns]


def run(spark, ingest_path, transformation_path):
    logging.info("Reading text file from: %s", ingest_path)
    input_df = spark.read.format("org.apache.spark.csv").option("header", True).csv(ingest_path)
    renamed_columns = sanitize_columns(input_df.columns)
    ref_df = input_df.toDF(*renamed_columns)
    ref_df.printSchema()
    ref_df.show()

    ref_df.write.parquet(transformation_path)
