docker build . -t test-spark-app --build-arg ARG_RUN_ACTION=tests -f Dockerfile
docker run -it test-spark-app