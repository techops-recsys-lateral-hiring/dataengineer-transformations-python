from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
import math

# Define the Haversine formula as a UDF (User Defined Function)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

haversine_udf = udf(haversine, FloatType())

def run(spark, dataset_path, output_path):
    # Read the dataset
    df = spark.read.csv(dataset_path, header=True, inferSchema=True)

    # Apply the Haversine UDF to calculate distances
    df = df.withColumn("distance", haversine_udf("start station latitude", "start station longitude", 
                                                 "end station latitude", "end station longitude"))

    # Write the results to the specified output path
    df.write.csv(output_path, header=True)
