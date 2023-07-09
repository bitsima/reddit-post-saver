'''
Provide the real-time check functionality to the app.

Functions:

real_time_check() -> None

'''
import time
import logging

from database_handling import database_handler
from logging_config import logging_config
from data_scraping import scraper

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)


def real_time_check() -> None:
    '''Works in the background in order to check the tracked subreddits for new posts each new second passed.'''

    # logging
    logger.info("Real-time check started with 1 second interval.")

    while True:
        subreddits_list = database_handler.get_subreddits_list()
        scraper.get_main_page()

        for sub in subreddits_list:
            latest_post_id = database_handler.get_latest_post_id(sub)

            new_posts = scraper.get_latest_posts(latest_post_id)

            if latest_post_id == "0":
                post = scraper.get_last_post()
                database_handler.add_to_db(post)

                # logging
                logger.info(
                    f"First post '{post.post_id}' added for the subreddit '{sub}'.")

                return

            for post in new_posts:
                database_handler.add_to_db(post)

                # logging
                logger.info(
                    f"Post '{post.post_id}' added to posts table from subreddit '{sub}'.")

        time.sleep(1)
