import unittest
import sys
from pyspark.sql import SparkSession
from pyspark.sql import Row

import thoughtworks.wordcount.utils as w


def dataframe_converter(df):
    col = df.columns
    collected_counts = df.collect()
    word_counts = []
    [word_counts.append((i.asDict().get(col[0]), i.asDict().get(col[1]))) for i in collected_counts]
    word_counts.sort
    return word_counts


class WordCountUtilsTest(unittest.TestCase):

    def setUp(self):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        self.spark = SparkSession.builder.appName("WordCountUtilsTest").getOrCreate()

    def tearDown(self):
        self.spark.stop()

    # Split Words
    @unittest.skip("Ignore test")
    def test_split_words_by_spaces(self):
        print("test_split_words_by_spaces")

    @unittest.skip("Ignore test")
    def test_split_words_by_period(self):
        print("test_split_words_by_period")

    @unittest.skip("Ignore test")
    def test_split_words_by_comma(self):
        print("test_split_words_by_comma")

    @unittest.skip("Ignore test")
    def test_split_words_by_hyphen(self):
        print("test_split_words_by_hyphen")

    @unittest.skip("Ignore test")
    def test_split_words_by_semicolon(self):
        print("test_split_words_by_semicolon")

    # Count Words
    @unittest.skip("Ignore test")
    def test_count_words_basic(self):
        print("test_count_words_basic")

    @unittest.skip("Ignore test")
    def test_should_not_aggregate_dissimilar_words(self):
        print("test_should_not_aggregate_dissimilar_words")

    @unittest.skip("Ignore test")
    def test_case_insensitivity(self):
        print("test_case_insensitivity")

    # Sort Words
    @unittest.skip("Ignore test")
    def test_ordering_words(self):
        print("test_ordering_words")


if __name__ == '__main__':
    unittest.main()
