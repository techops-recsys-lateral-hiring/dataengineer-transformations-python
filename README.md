# Data transformations with Python
This is a collection of _Python_ jobs that are supposed to transform data.
These jobs are using _PySpark_ to process larger volumes of data and are supposed to run on a Spark cluster (via `spark-submit`).

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
file (corpus). 

There is a dump of the datalake for this under `resources/word_count/words.txt` with a text file.

#### Input
Simple `*.txt` file containing text.

#### Output
A single `*.csv` file containing data similar to:
```csv
"word","count"
"a","3"
"an","5"
...
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
For analytics purposes the BI department of a bike share company would like to present dashboards, displaying the
distance each bike was driven. There is a `*.csv` file that contains historical data of previous bike rides. This input
file needs to be processed in multiple steps. There is a pipeline running these jobs.

![citibike pipeline](docs/citibike.png)

There is a dump of the datalake for this under `resources/citibike/citibike.csv` with historical data.

#### Ingest
Reads a `*.csv` file and transforms it to parquet format. The column names will be sanitized (whitespaces replaced).

##### Input
Historical bike ride `*.csv` file:
```csv
"tripduration","starttime","stoptime","start station id","start station name","start station latitude",...
364,"2017-07-01 00:00:00","2017-07-01 00:06:05",539,"Metropolitan Ave & Bedford Ave",40.71534825,...
...
```

##### Output
`*.parquet` files containing the same content
```csv
"tripduration","starttime","stoptime","start_station_id","start_station_name","start_station_latitude",...
364,"2017-07-01 00:00:00","2017-07-01 00:06:05",539,"Metropolitan Ave & Bedford Ave",40.71534825,...
...
```

##### Run the job
Please make sure to package the code before submitting the spark job (`pipenv run packager`)
```bash
pipenv run spark-submit \
    --master local \
    --py-files dist/data_transformations-0.1.0-py3.6.egg \
    jobs/citibike_ingest.py \
    <INPUT_FILE_PATH> \
    <OUTPUT_PATH>
```

#### Distance calculation
This job takes bike trip information and calculates the "as the crow flies" distance traveled for each trip.
It reads the previously ingested data parquet files.

Hint:
 - For distance calculation, consider using [**Harvesine formula**](https://en.wikipedia.org/wiki/Haversine_formula) as an option.  

##### Input
Historical bike ride `*.parquet` files
```csv
"tripduration",...
364,...
...
```

##### Outputs
`*.parquet` files containing historical data with distance column containing the calculated distance.
```csv
"tripduration",...,"distance"
364,...,1.34
...
```

##### Run the job
Please make sure to package the code before submitting the spark job (`pipenv run packager`)
```bash
pipenv run spark-submit \
    --master local \
    --py-files dist/data_transformations-0.1.0-py3.6.egg \
    jobs/citibike_distance_calculation.py \
    <INPUT_PATH> \
    <OUTPUT_PATH>
```
