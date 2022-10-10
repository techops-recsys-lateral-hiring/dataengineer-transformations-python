#!/bin/bash

set -euo pipefail

poetry build

jobName=$(echo "${JOB}" | awk '{ print tolower($1) }')

if [[ "${jobName}" == "citibike_ingest" ]]; then
    INPUT_FILE_PATH="./resources/citibike/citibike.csv"
    JOB_ENTRY_POINT="jobs/citibike_ingest.py"
    OUTPUT_PATH="./output_int"
elif [[ "${jobName}" == "citibike_distance_calculation" ]]; then
    INPUT_FILE_PATH="./output_int"
    JOB_ENTRY_POINT="jobs/citibike_distance_calculation.py"
    OUTPUT_PATH="./output"
elif [[ "${jobName}" == "wordcount" ]]; then
    INPUT_FILE_PATH="./resources/word_count/words.txt"
    JOB_ENTRY_POINT="jobs/word_count.py"
    OUTPUT_PATH="./output"
else
  echo "Job name provided was : ${JOB} : failed"
  echo "Job name deduced was : ${jobName} : failed"
  echo "Please enter a valid job name (citibike_ingest, citibike_distance_calculation or wordcount)"
  exit 1
fi

rm -rf $OUTPUT_PATH



poetry run spark-submit \
    --master local \
    --py-files dist/data_transformations-*.whl \
    $JOB_ENTRY_POINT \
    $INPUT_FILE_PATH \
    $OUTPUT_PATH

