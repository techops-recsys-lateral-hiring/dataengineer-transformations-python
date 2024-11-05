import csv
import os
import tempfile
from typing import Tuple, List

from pyspark.sql import SparkSession

from data_transformations.citibike import ingest


def test_should_sanitize_column_names(spark_session: SparkSession) -> None:
    given_ingest_folder, given_transform_folder = __create_ingest_and_transform_folders()
    input_csv_path = given_ingest_folder + 'input.csv'
    csv_content = [
        ['first_field', 'field with space', ' fieldWithOuterSpaces '],
        ['3', '4', '1'],
        ['1', '5', '2'],
    ]
    __write_csv_file(input_csv_path, csv_content)
    ingest.run(spark_session, input_csv_path, given_transform_folder)

    actual = spark_session.read.parquet(given_transform_folder)
    expected = spark_session.createDataFrame(
        [
            ['3', '4', '1'],
            ['1', '5', '2']
        ],
        ['first_field', 'field_with_space', '_fieldWithOuterSpaces_']
    )

    assert expected.collect() == actual.collect()


def __create_ingest_and_transform_folders() -> Tuple[str, str]:
    base_path = tempfile.mkdtemp()
    ingest_folder = "%s%s" % (base_path, os.path.sep)
    transform_folder = "%s%stransform" % (base_path, os.path.sep)
    return ingest_folder, transform_folder


def __write_csv_file(file_path: str, content: List[List[str]]) -> None:
    with open(file_path, 'w') as csv_file:
        input_csv_writer = csv.writer(csv_file)
        input_csv_writer.writerows(content)
        csv_file.close()
