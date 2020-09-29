import unittest
import sys, os, shutil
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions as F

import thoughtworks.citibike.CitibikeTransformer as CitibikeTransformer

citibikeBaseDataColumns = [
    "tripduration", "starttime", "stoptime", "start_station_id", "start_station_name", "start_station_latitude",
    "start_station_longitude", "end_station_id", "end_station_name", "end_station_latitude", "end_station_longitude",
    "bikeid", "usertype", "birth_year", "gender"]

sampleCitibikeData = [
    [328, "2017-07-01 00:00:08", "2017-07-01 00:05:37", 3242, "Schermerhorn St & Court St", 40.69102925677968,
     -73.99183362722397, 3397, "Court St & Nelson St", 40.6763947, -73.99869893, 27937, "Subscriber", 1984, 2],
    [1496, "2017-07-01 00:00:18", "2017-07-01 00:25:15", 3233, "E 48 St & 5 Ave", 40.75724567911726, -73.97805914282799,
     546, "E 30 St & Park Ave S", 40.74444921, -73.98303529, 15933, "Customer", 1971, 1],
    [1067, "2017-07-01 00:16:31", "2017-07-01 00:34:19", 448, "W 37 St & 10 Ave", 40.75660359, -73.9979009, 487,
     "E 20 St & FDR Drive", 40.73314259, -73.97573881, 27084, "Subscriber", 1990, 2]
]

class CitibikeTransformerTest(unittest.TestCase):

    def setUp(self):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        self.spark = SparkSession.builder.appName("CitibikeTransformerTest").getOrCreate()

    def tearDown(self):
        self.spark.stop()

    # CitibikeTransformer application

    #@unittest.skip("Ignore test")
    def test_acceptance_for_basic_use(self):
        print("test_acceptance_for_basic_use")
        root_directory = os.getcwd()
        data_directory = root_directory + "/Citibike"
        ingest_directory = data_directory + "/ingest"
        os.makedirs(ingest_directory, exist_ok=False)
        transform_directory = data_directory + "/transform"
        os.makedirs(transform_directory, exist_ok=False)
        input_DF = self.spark.createDataFrame(sampleCitibikeData, citibikeBaseDataColumns)
        input_DF.write.parquet(ingest_directory, mode='append')
        # Run test app
        CitibikeTransformer.run(self.spark, ingest_directory, transform_directory)
        transformed_DF = self.spark.read.parquet(transform_directory)
        expected_columns = set(citibikeBaseDataColumns)
        new_columns = set(transformed_DF.select(*citibikeBaseDataColumns).columns)
        input = set(input_DF.schema)
        transformed = set(transformed_DF.schema)
        #Restore directories to original state
        shutil.rmtree(data_directory)
        os.chdir(root_directory)
        #New data should have all of the old data
        #Check columns
        with self.subTest():
            self.assertEqual(new_columns, expected_columns)
        #Check schema
        with self.subTest():
            self.assertTrue(input.issubset(transformed))

    #@unittest.skip("Ignore test")
    def test_acceptance_for_advanced_use(self):
        print("test_acceptance_for_advanced_use")
        root_directory = os.getcwd()
        print(root_directory)
        data_directory = root_directory + "/Citibike"
        ingest_directory = data_directory + "/ingest"
        os.makedirs(ingest_directory, exist_ok=False)
        transform_directory = data_directory + "/transform"
        os.makedirs(transform_directory, exist_ok=False)
        input_DF = self.spark.createDataFrame(sampleCitibikeData, citibikeBaseDataColumns)
        input_DF.write.parquet(ingest_directory, mode='append')
        # Run test app
        CitibikeTransformer.run(self.spark, ingest_directory, transform_directory)
        transformed_DF = self.spark.read.parquet(transform_directory)
        transformed_sorted_DF = transformed_DF.sort(F.col("tripduration"))
        actual_data = transformed_sorted_DF.collect()
        expectedData = [
            Row(328, "2017-07-01 00:00:08", "2017-07-01 00:05:37", 3242, "Schermerhorn St & Court St",
                40.69102925677968, -73.99183362722397, 3397, "Court St & Nelson St", 40.6763947, -73.99869893, 27937,
                "Subscriber", 1984, 2, 1.07),
            Row(1496, "2017-07-01 00:00:18", "2017-07-01 00:25:15", 3233, "E 48 St & 5 Ave", 40.75724567911726,
                -73.97805914282799, 546, "E 30 St & Park Ave S", 40.74444921, -73.98303529, 15933, "Customer", 1971, 1,
                0.92),
            Row(1067, "2017-07-01 00:16:31", "2017-07-01 00:34:19", 448, "W 37 St & 10 Ave", 40.75660359, -73.9979009,
                487, "E 20 St & FDR Drive", 40.73314259, -73.97573881, 27084, "Subscriber", 1990, 2.0, 1.99)]
        expectedData.sort()
        #Restore directories to original state
        shutil.rmtree(data_directory)
        os.chdir(root_directory)
        for i in range(0, len(expectedData)):
            for j in range(0, len(expectedData[i])):
                with self.subTest((i, j)):
                    self.assertEqual(actual_data[i][j], expectedData[i][j])


if __name__ == '__main__':
    unittest.main()