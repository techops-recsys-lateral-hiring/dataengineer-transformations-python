import os
import tempfile
from typing import Tuple

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, DoubleType

from data_transformations.citibike import distance_transformer

BASE_COLUMNS = [
    "tripduration",
    "starttime",
    "stoptime",
    "start_station_id",
    "start_station_name",
    "start_station_latitude",
    "start_station_longitude",
    "end_station_id",
    "end_station_name",
    "end_station_latitude",
    "end_station_longitude",
    "bikeid",
    "usertype",
    "birth_year",
    "gender",
]

SAMPLE_DATA = [
    [
        328,
        "2017-07-01 00:00:08",
        "2017-07-01 00:05:37",
        3242,
        "Schermerhorn St & Court St",
        40.69102925677968,
        -73.99183362722397,
        3397,
        "Court St & Nelson St",
        40.6763947,
        -73.99869893,
        27937,
        "Subscriber",
        1984,
        2
    ],
    [
        1496,
        "2017-07-01 00:00:18",
        "2017-07-01 00:25:15",
        3233,
        "E 48 St & 5 Ave",
        40.75724567911726,
        -73.97805914282799,
        546,
        "E 30 St & Park Ave S",
        40.74444921,
        -73.98303529,
        15933,
        "Customer",
        1971,
        1
    ],
    [
        1067,
        "2017-07-01 00:16:31",
        "2017-07-01 00:34:19",
        448,
        "W 37 St & 10 Ave",
        40.75660359,
        -73.9979009,
        487,
        "E 20 St & FDR Drive",
        40.73314259,
        -73.97573881,
        27084,
        "Subscriber",
        1990,
        2
    ]
]


def test_should_maintain_all_data_it_reads(spark_session: SparkSession) -> None:
    given_ingest_folder, given_transform_folder = __create_ingest_and_transform_folders(
        spark_session)
    given_dataframe = spark_session.read.parquet(given_ingest_folder)
    distance_transformer.run(spark_session, given_ingest_folder, given_transform_folder)

    actual_dataframe = spark_session.read.parquet(given_transform_folder)
    actual_columns = set(actual_dataframe.columns)
    actual_schema = set(actual_dataframe.schema)
    expected_columns = set(given_dataframe.columns)
    expected_schema = set(given_dataframe.schema)

    assert expected_columns == actual_columns
    assert expected_schema.issubset(actual_schema)


@pytest.mark.skip
def test_should_add_distance_column_with_calculated_distance(spark_session: SparkSession) -> None:
    given_ingest_folder, given_transform_folder = __create_ingest_and_transform_folders(
        spark_session)
    distance_transformer.run(spark_session, given_ingest_folder, given_transform_folder)

    actual_dataframe = spark_session.read.parquet(given_transform_folder)
    expected_dataframe = spark_session.createDataFrame(
        [
            SAMPLE_DATA[0] + [1.07],
            SAMPLE_DATA[1] + [0.92],
            SAMPLE_DATA[2] + [1.99],
        ],
        BASE_COLUMNS + ['distance']
    )
    expected_distance_schema = StructField('distance', DoubleType(), nullable=True)
    actual_distance_schema = actual_dataframe.schema['distance']

    assert expected_distance_schema == actual_distance_schema
    assert expected_dataframe.collect() == actual_dataframe.collect()


def __create_ingest_and_transform_folders(spark: SparkSession) -> Tuple[str, str]:
    base_path = tempfile.mkdtemp()
    ingest_folder = "%s%singest" % (base_path, os.path.sep)
    transform_folder = "%s%stransform" % (base_path, os.path.sep)
    ingest_dataframe = spark.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
    ingest_dataframe.write.parquet(ingest_folder, mode='overwrite')
    return ingest_folder, transform_folder
