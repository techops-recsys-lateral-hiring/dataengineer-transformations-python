import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

meters_per_foot = 0.3048
feet_per_mile = 5280
earth_radius_in_meters = 6371e3
meters_per_mile = meters_per_foot * feet_per_mile


def compute_distance(spark, dataframe):
    return dataframe
