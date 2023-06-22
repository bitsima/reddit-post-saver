import time
import logging
from database_handling import database_handler
from logging_config import logging_config

logging_config.configure_logging()
logger = logging.getLogger(__name__)


def real_time_check(reddit):

    # logging
    logger.info("Real-time check started with 1 second interval.")

    while True:
        subreddits_list = database_handler.get_subreddits_list()
        for sub in subreddits_list:

            posts_reddit = reddit.subreddit(sub).new()
            latest_post_id = database_handler.get_latest_post_id(sub)

            if latest_post_id == "0":
                post = list(reddit.subreddit(sub).new(limit=1))
                database_handler.add_to_db(post[0])

                # logging
                logger.info(
                    f"First post '{post[0].id}' added for the subreddit '{sub}'.")

                return

            for post in posts_reddit:
                print(post.id, " ", latest_post_id)
                if post.id == latest_post_id:
                    break
                database_handler.add_to_db(post)

                # logging
                logger.info(
                    f"Post '{post.id}' added to posts table from subreddit '{sub}'.")

        time.sleep(1)
