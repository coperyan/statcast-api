import configparser
import logging
import logging.config
from datetime import datetime, timedelta
from pathlib import Path
import time

from .client import BaseballSavant
from .data import BaseballSavantData

# Setting up logger, Logger properties are defined in logging.ini file
logging.config.fileConfig(f"{Path(__file__).parents[0]}/logging.ini")
logger = logging.getLogger(__name__)

# Reading configurations
config = configparser.ConfigParser()
config.read_file(open("config.cfg"))


def main():
    logging.debug("Creating baseball savant client.")
    bsclient = BaseballSavant()
    bsdata = BaseballSavantData(bsclient, config["DATA_DIR_PATH"]["PATH"])

    end_after = int(config["TIMEPARAM"]["END_TIME"])
    wait_time = int(config["TIMEPARAM"]["WAIT_TIME"])

    logging.debug(f"Execution started at {datetime.now()}")
    end_time = datetime.now() + timedelta(seconds=end_after)
    logging.debug(f"Execution will end at : {end_time}")

    while datetime.now() < end_time:
        logging.debug("Fetching data.....")
        try:
            bsdata.fetch_data()
        except Exception as e:
            logging.exception("Some exception occured : ", e)
            continue

        logging.debug(f"Waiting for {config['TIMEPARAM']['WAIT_TIME']} seconds")
        time.sleep(wait_time)

    logging.debug("Execution ended.")


if __name__ == "__main__":
    main()
    logging.debug("Exiting.")
