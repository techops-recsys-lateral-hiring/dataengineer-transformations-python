# Data transformations with Python
This is a collection of _Python_ jobs that are supposed to transform data.
These jobs are using _PySpark_ to process larger volumes of data and are supposed to run on a _Spark_ cluster (via `spark-submit`).

## Pre-requisites

We use [`batect`](https://batect.dev/) to dockerise the tasks in this exercise. 
`batect` is a lightweight wrapper around Docker that helps to ensure tasks run consistently (across linux, mac windows).
With `batect`, the only dependencies that need to be installed are Docker and Java >=8. Every other dependency is managed inside Docker containers.
If docker desktop can't be installed then Colima could be used on Mac and Linux. 

> **For Windows, docker desktop is the only option for using container to run application
otherwise local laptop should be set up.**

Please make sure you have the following installed and can run them
* Docker Desktop or Colima
* Java (11)

You could use following instructions as guidelines to install Docker or Colima and Java.

```bash
# Install pre-requisites needed by batect 
# For mac users: 
./go.sh install-with-docker-desktop
OR
./go.sh install-with-colima

# For windows/linux users:
# Please ensure Docker and java >=8 is installed 
scripts\install_choco.ps1
scripts\install.bat

# For local laptop setup ensure that Java 11 with Spark 3.2.1 is available. More details in README-LOCAL.md
```

> **If you are using Colima, please ensure that you start Colima. For staring Colima, you could use following command:**

`./go.sh start-colima`


## List of commands

General pattern apart from installation and starting of Colima is:

`./go.sh run-<type>-<action>`

type could be local, colima or docker-desktop

action could be unit-test, integration-test or job.

Full list of commands for Mac and Linux users is as follows: 

| S.No.      | Command | Action     |
| :---:        |    :----   |          :--- |
| 1      | ./go.sh lint       | Static analysis, code style, etc.   |
| 2      | ./go.sh linting       | Static analysis, code style, etc.   |
| 3      | ./go.sh install-with-docker-desktop       | Install the application requirements along with docker desktop   |
| 4      | ./go.sh install-with-colima       | Install the application requirements along with colima   |
| 5      | ./go.sh start-colima       | Start Colima   |
| 6      | ./go.sh run-local-unit-test       | Run unit tests on local machine   |
| 7      | ./go.sh run-colima-unit-test       | Run unit tests on containers using Colima   |
| 8      | ./go.sh run-docker-desktop-unit-test       | Run unit tests on containers using Docker Desktop   |
| 9      | ./go.sh run-local-integration-test       | Run integration tests on local machine   |
| 10      | ./go.sh run-colima-integration-test       | Run integration tests on containers using Colima   |
| 11     | ./go.sh run-docker-desktop-integration-test       | Run integration tests on containers using Docker Desktop   |
| 12     | ./go.sh run-local-job       | Run job on local machine   |
| 13     | ./go.sh run-colima-job       | Run job on containers using Colima   |
| 14     | ./go.sh run-docker-desktop-job       | Run job on containers using Docker Desktop   |
| 15     | ./go.sh Usage       | Display usage   |


Full list of commands for Windows users is as follows:

| S.No.      | Command | Action     |
| :---:        |    :----   |          :--- |
| 1      | go.ps1 linting       | Static analysis, code style, etc.   |
| 2      | go.ps1 install-with-docker-desktop       | Install the application requirements along with docker desktop   |
| 3      | go.ps1 run-local-unit-test       | Run unit tests on local machine   |
| 4      | go.ps1 run-docker-desktop-unit-test       | Run unit tests on containers using Docker Desktop   |
| 5      | go.ps1 run-local-integration-test       | Run integration tests on local machine   |
| 6     | go.ps1 run-docker-desktop-integration-test       | Run integration tests on containers using Docker Desktop   |
| 7     | go.ps1 run-local-job       | Run job on local machine   |
| 8     | go.ps1 run-docker-desktop-job       | Run job on containers using Docker Desktop   |
| 9     | go.ps1 Usage       | Display usage   |


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

#### Run the job using Docker Desktop on Mac or Linux

```bash
JOB=wordcount ./go.sh run-docker-desktop-job 
```

#### Run the job using Docker Desktop on Windows

```bash
JOB=wordcount go.ps1 run-docker-desktop-job 
```

#### Run the job using Colima

```bash
JOB=wordcount ./go.sh run-colima-job 
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

##### Run the job using Docker Desktop on Mac or Linux

```bash
JOB=citibike_ingest ./go.sh run-docker-desktop-job
```

##### Run the job using Docker Desktop on Windows

```bash
JOB=citibike_ingest go.ps1 run-docker-desktop-job
```

##### Run the job using Colima

```bash
JOB=citibike_ingest ./go.sh run-colima-job
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

##### Run the job using Docker Desktop on Mac or Linux

```bash
JOB=citibike_distance_calculation ./go.sh run-docker-desktop-job
```

##### Run the job using Docker Desktop on Windows

```bash
JOB=citibike_distance_calculation go.ps1 run-docker-desktop-job
```

##### Run the job using Colima

```bash
JOB=citibike_distance_calculation ./go.sh run-colima-job
```


## Running the code outside container

If you would like to run the code in your laptop locally without containers then please follow instructions [here](README-LOCAL.md).
