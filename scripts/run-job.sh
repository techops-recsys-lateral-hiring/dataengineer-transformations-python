#!/bin/bash

set -e

poetry build

INPUT_FILE_PATH="./resources/citibike/citibike.csv"
OUTPUT_PATH="./output"

rm -rf $OUTPUT_PATH

poetry run spark-submit \
    --master local \
    --py-files dist/data_transformations-*.whl \
    $JOB \
    $INPUT_FILE_PATH \
    $OUTPUT_PATH