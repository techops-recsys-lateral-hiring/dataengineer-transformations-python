import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def SPARK() -> SparkSession:
    return SparkSession.builder.appName("IntegrationTests").getOrCreate()
