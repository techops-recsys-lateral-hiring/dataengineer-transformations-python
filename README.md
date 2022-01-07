# Data transformations with Python
This is a collection of _Python_ jobs that are supposed to transform data.
These jobs are using _PySpark_ to process larger volumes of data and are supposed to run on a _Spark_ cluster (via `spark-submit`).

## Pre-requisites

We use [`batect`](https://batect.dev/) to dockerise the tasks in this exercise. 
`batect` is a lightweight wrapper around Docker that helps to ensure tasks run consistently (across linux, mac windows).
With `batect`, the only dependencies that need to be installed are Docker and Java >=8. Every other dependency is managed inside Docker containers.
Please make sure you have the following installed and can run them
* Docker
* Java >= (1.8)

You could use following instructions as guidelines to install Docker and Java.

```bash
# Install pre-requisites needed by batect 
# For mac users: 
scripts/install.sh

# For windows/linux users:
# Please ensure Docker and java >=8 is installed 
scripts\install_choco.ps1
scripts\install.bat
```

## Run tests

### Run unit tests
```bash
./batect unit-test
```

### Run integration tests
```bash
./batect integration-test
```

## Run style checks
```bash
./batect style-checks
```
This is running the linter and a type checker.

## Jobs

There are two applications in this repo: Word Count, and Citibike.

Currently, these exist as skeletons, and have some initial test cases which are defined but ignored.
For each application, please un-ignore the tests and implement the missing logic.

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

```bash
JOB=jobs/word_count.py ./batect run-job 
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

```bash
JOB=jobs/citibike_ingest.py ./batect run-job
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

```bash
JOB=jobs/citibike_distance_calculation.py ./batect run-job
```

## Running the code outside container

If you would like to run the code in your laptop locally without containers then please follow instructions [here](README-LOCAL.md).
