from pyspark.sql.functions import explode, lower, regexp_replace, col
from pyspark.sql import SparkSession

def run(spark: SparkSession, input_path: str, output_path: str):
    # Read the input text file into a DataFrame
    df = spark.read.text(input_path)

    # Process the text to count words
    # - Convert to lowercase
    # - Remove non-word characters
    # - Split lines into individual words
    # - Group by word and count occurrences
    word_counts = (df.select(explode(lower(regexp_replace(col("value"), "[^a-zA-Z\\s]", "")).split(" ")).alias("word"))
                     .groupBy("word")
                     .count()
                     .sort("count", ascending=False))

    # Write the results to the specified output path
    word_counts.write.csv(output_path, header=True)
