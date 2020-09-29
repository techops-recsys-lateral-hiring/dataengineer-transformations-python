import logging
import sys

from data_transformations import wordcount_main, citibike_main, daily_driver_main

if __name__ == '__main__':

    LOG_FILENAME = 'project.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

    for num, name in enumerate(sys.argv, start=0):
        print("args {}: {}".format(num, name))

    job_name = None
    if len(sys.argv) > 1:
        job_name = sys.argv[1]
        print(job_name)
    else:
        print("No job name supplied. Please specify WordCount, CitiBike or DailyDriver")
        logging.warning("No job name supplied. Please specify WordCount, CitiBikeTransformer or DailyDriver")
        sys.exit(1)
    if job_name == "WordCount":
        wordcount_main.main(sys.argv)
    elif job_name == "CitiBikeTransformer":
        citibike_main.main(sys.argv)
    elif job_name == "DailyDriver":
        daily_driver_main.main(sys.argv)
