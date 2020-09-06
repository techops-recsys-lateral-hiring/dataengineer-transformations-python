from pyspark.sql import functions as F

METERS_PER_FOOT = 0.3048
FEET_PER_MILE = 5280
EARTH_RADIUS_METERS = 6371e3
METERS_PER_MILE = METERS_PER_FOOT * FEET_PER_MILE


def compute_distances(spark, dataframe):
    return dataframe
