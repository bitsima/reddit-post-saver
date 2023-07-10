import threading
import logging
import os

from logging_config import logging_config
from realtime_crawling import threader
from database_handling import database_handler
from user_interface import prompter

# configuring the Logger object
logging_config.configure_logging()
logger = logging.getLogger(__name__)

os.system("clear")

print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n Hi! The system is initializing... Please wait.\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
logger.info("Program started.")

database_handler.create_db()

if __name__ == "__main__":
    t1 = threading.Thread(target=threader.real_time_check)
    t1.start()
    while True:  # we need the checks to run as long as the program is running
        try:
            prompter.interact()
        except Exception as error:
            print("An error occurred: ", error)

            # logging
            logger.error(f"An error occurred: {error}")
