import csv
import os
import tempfile

from data_transformations.citibike import DailyDriver
from tests.citibike import SPARK


def test_should_transform_csv_to_parquet_and_replace_whitespaces_from_column_names():
    given_ingest_folder, given_transform_folder = create_ingest_and_transform_folders()
    input_csv_path = given_ingest_folder + 'input.csv'
    csv_content = [
        ['first_field', 'field with space', ' fieldWithOuterSpaces '],
        ['3', '1', '4'],
        ['1', '5', '2'],
    ]
    write_csv_file(input_csv_path, csv_content)
    DailyDriver.run(SPARK, input_csv_path, given_transform_folder)

    actual = SPARK.read.parquet(given_transform_folder)
    expected_columns = ['first_field', 'field_with_space', '_fieldWithOuterSpaces_']

    assert 2 == actual.count()
    assert expected_columns == actual.columns


def create_ingest_and_transform_folders():
    base_path = tempfile.mkdtemp()
    ingest_folder = "%s%s" % (base_path, os.path.sep)
    transform_folder = "%s%stransform" % (base_path, os.path.sep)
    return ingest_folder, transform_folder


def write_csv_file(file_path, content):
    with open(file_path, 'w') as csv_file:
        input_csv_writer = csv.writer(csv_file)
        input_csv_writer.writerows(content)
        csv_file.close()
