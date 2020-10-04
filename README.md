# Data transformations with Python
This is a collection of _Python_ jobs that are supposed to transform data.
These jobs are using _PySpark_ to process larger volumes of data. These jobs are supposed to run on a Spark cluster.

## Pre-requisites
Please make sure you have the following installed and can run them
* Python (3.6 or later)
* Pipenv
* Java (1.8 or later)

## Install all dependencies
```bash
pipenv install
```

## Run tests
### Run unit tests
```bash
pipenv run unit-test
```

### Run unit tests
```bash
pipenv run integration-test
```

## Create .egg package
```bash
pipenv run packager
```

## Use linter
```bash
pipenv run linter
```
## Jobs
### Word Count
A NLP model is dependent on a specific input file. This job is supposed to preprocess a given text file to produce this
input file for the NLP model (feature engineering). This job will count the occurrences of a word within the given text
file. 

There is a dump of the datalake for this under `resources/word_count/words.txt` with a text file.

#### Input
Simple `*.txt` file containing text.

#### Output
A single `*.csv` file containing data similar to:
```csv
"word","count"
"a","3"
"an","5"
```

#### Run the job
Please make sure to package the code before submitting the spark job (`pipenv run packager`)
```bash
pipenv run spark-submit \
    --master local \
    --py-files dist/data_transformations-0.1.0-py3.6.egg \
    jobs/word_count.py \
    <INPUT_FILE_PATH> \
    <OUTPUT_PATH>
```

### Citibike
* Sample data is available in the `src/test/citibike/data` directory
This application takes bike trip information and calculates the "as the crow flies" distance traveled for each trip.  
The application is run in two steps.
* First the data will be ingested from a sources and transformed to parquet format.
* Then the application will read the parquet files and apply the appropriate transformations.


* To ingest data from external source to datalake - make sure to package all dependencies first:
```
spark-submit --py-files dist/data_transformations-0.1.0-py3.6.egg --master local citibike_ingest.py $(INPUT_CSV_FILE) $(OUTPUT_LOCATION)
```

* To transform Citibike data:
```
spark-submit --py-files dist/data_transformations-0.1.0-py3.6.egg --master local citibike_distance_calculation.py $(INPUT_DATASET_LOCATION) $(OUTPUT_LOCATION)
```

Currently this application is a skeleton with ignored tests.  Please unignore the tests and build the Citibike transformation application.

#### Tips
- For distance calculation, consider using [**Harvesine formula**](https://en.wikipedia.org/wiki/Haversine_formula) as an option.  
