from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

METERS_PER_FOOT = 0.3048
FEET_PER_MILE = 5280
EARTH_RADIUS_IN_METERS = 6371e3
METERS_PER_MILE = METERS_PER_FOOT * FEET_PER_MILE


def computeDistances(spark, dataframe):
    df = dataframe.withColumn("lat1",F.radians(F.col("start_station_latitude"))).withColumn("lat2",F.radians(F.col("end_station_latitude")))\
        .withColumn("lon1",F.radians(F.col("start_station_longitude"))).withColumn("lon2",F.radians(F.col("end_station_longitude")))\
        .withColumn("distance",F.round(F.asin(F.sqrt(
            (-F.cos(F.col("lat2") - F.col("lat1"))*0.5 + 0.5) +
              F.cos(F.col("lat1"))*
                F.cos(F.col("lat2"))*
                (-F.cos(F.col("lon2") - F.col("lon1"))*0.5 + 0.5)))
                  *(2*EARTH_RADIUS_IN_METERS/METERS_PER_MILE),2))
    df = df.drop(F.col("lat1")).drop(F.col("lat2")).drop(F.col("lon1")).drop(F.col("lon2"))
    return df
