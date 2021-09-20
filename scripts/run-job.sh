#!/bin/bash

set -e

poetry build

INPUT_FILE_PATH="./resources/citibike/citibike.csv"
OUTPUT_PATH="./output"

poetry run spark-submit \
    --master local \
    --py-files dist/data_transformations-*.whl \
    jobs/word_count.py \
    $INPUT_FILE_PATH \
    $OUTPUT_PATH