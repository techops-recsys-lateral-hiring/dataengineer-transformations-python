import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    return SparkSession.builder.appName("IntegrationTests").getOrCreate()
