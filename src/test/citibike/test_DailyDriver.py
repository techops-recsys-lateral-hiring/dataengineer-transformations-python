import unittest
import sys, os, shutil
from pyspark.sql import SparkSession

import thoughtworks.citibike.DailyDriver as DailyDriver


class DailyDriverTest(unittest.TestCase):

    def setUp(self):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        self.spark = SparkSession.builder.appName("DailyDriverTest").getOrCreate()

    def tearDown(self):
        self.spark.stop()

    @unittest.skip("Ignore test")
    def test_daily_driver_ingestion(self):
        print("test_daily_driver_ingestion")
        root_directory = os.getcwd()
        file_directory = root_directory + "/test-result"
        os.makedirs(file_directory, exist_ok=False)
        # Create input file
        input_csv = file_directory + "/input.csv"
        output_directory = root_directory + "/output"
        lines = ["first_field,field with space, fieldWithOuterSpaces ", "3,1,4", "1,5,2"]
        with open(input_csv, 'w') as f:
            for line in lines:
                print(line, file=f)
        DailyDriver.run(self.spark, input_csv, output_directory)
        # Read results
        parquet_directory = self.spark.read.parquet(output_directory)
        parquet_directory_count = parquet_directory.count()
        with self.subTest():
            self.assertEqual(parquet_directory_count, 2)
        parquet_directory_columns = parquet_directory.columns
        expected_column_headings = ["first_field", "field_with_space", "_fieldWithOuterSpaces_"]
        # Restore directories to original state
        shutil.rmtree(file_directory)
        shutil.rmtree(output_directory)
        os.chdir(root_directory)
        with self.subTest():
            self.assertEqual(parquet_directory_columns, expected_column_headings)


if __name__ == '__main__':
    unittest.main()
