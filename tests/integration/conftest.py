import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def SPARK():
    return SparkSession.builder.appName("IntegrationTests").getOrCreate()
