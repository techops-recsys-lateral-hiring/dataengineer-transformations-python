import csv
import os
import tempfile

from data_transformations.citibike import ingest
from tests.integration import SPARK


def test_should_do_nothing_for_no_whitespace_in_column_name():
    given_ingest_folder, given_transform_folder = __create_ingest_and_transform_folders()
    input_csv_path = given_ingest_folder + 'input.csv'
    csv_content = [
        ['first_field'],
        ['3'],
        ['1'],
    ]
    __write_csv_file(input_csv_path, csv_content)
    ingest.run(SPARK, input_csv_path, given_transform_folder)

    actual = SPARK.read.parquet(given_transform_folder)
    expected = SPARK.createDataFrame([['3'], ['1']], csv_content[0])

    assert expected.collect() == actual.collect()


def test_should_replace_whitespace_in_between_column_name():
    given_ingest_folder, given_transform_folder = __create_ingest_and_transform_folders()
    input_csv_path = given_ingest_folder + 'input.csv'
    csv_content = [
        ['first field'],
        ['3'],
        ['1'],
    ]
    __write_csv_file(input_csv_path, csv_content)
    ingest.run(SPARK, input_csv_path, given_transform_folder)

    actual = SPARK.read.parquet(given_transform_folder)
    expected = SPARK.createDataFrame([['3'], ['1']], ['first_field'])

    assert expected.collect() == actual.collect()


def test_should_replace_whitespace_outside_column_name():
    given_ingest_folder, given_transform_folder = __create_ingest_and_transform_folders()
    input_csv_path = given_ingest_folder + 'input.csv'
    csv_content = [
        [' first_field '],
        ['3'],
        ['1'],
    ]
    __write_csv_file(input_csv_path, csv_content)
    ingest.run(SPARK, input_csv_path, given_transform_folder)

    actual = SPARK.read.parquet(given_transform_folder)
    expected = SPARK.createDataFrame([['3'], ['1']], ['_first_field_'])

    assert expected.collect() == actual.collect()


def __create_ingest_and_transform_folders():
    base_path = tempfile.mkdtemp()
    ingest_folder = "%s%s" % (base_path, os.path.sep)
    transform_folder = "%s%stransform" % (base_path, os.path.sep)
    return ingest_folder, transform_folder


def __write_csv_file(file_path, content):
    with open(file_path, 'w') as csv_file:
        input_csv_writer = csv.writer(csv_file)
        input_csv_writer.writerows(content)
        csv_file.close()
