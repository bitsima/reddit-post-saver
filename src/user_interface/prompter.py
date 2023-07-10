import logging

from database_handling import database_handler
from data_scraping import scraper
from logging_config import logging_config

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)


def interact() -> None:
    # keeping the tracked subreddit list up to date with the database
    tracked_subreddits = database_handler.get_subreddits_list()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(''' | 1 - See the tracking list
 | 2 - Edit the tracking list
 | 3 - See saved posts''')
    choice = input("What would you like to do? Please enter a number: \n")

    match choice:
        case "1":  # See the tracking list
            print("Here's the tracked subreddits list:")
            for count, sub in enumerate(tracked_subreddits):
                print(str(count) + " - " + sub)

        case "2":  # Edit the tracking list
            edit_tracking()

        case "3":  # See saved posts'
            for count, sub in enumerate(tracked_subreddits):
                print(str(count) + " - " + sub)

            subIndex = int(input(
                "Here's the tracked subreddits list. Please enter the number of the one you want to see the last 10 saved posts of: ")) - 1
            try:
                sub = tracked_subreddits[subIndex]
            except IndexError:
                print("Not a valid number!")
            if sub in tracked_subreddits:
                database_handler.print_posts_from_subreddit(sub)

        case _:
            "Not a valid choice!"


def subreddit_check() -> str:
    '''Checks if the given subreddit name is true.'''
    subreddit = input(
        "Please provide a keyword for the subreddit you want to search for:\n")

    # logging
    logger.info(f"Started search for subreddit named '{subreddit}'.")

    error_occurred = scraper.get_main_page(subreddit)

    if error_occurred:
        print("That's not a valid subreddit name!")
        return

    # logging
    logger.info(f"Chosen subreddit '{subreddit.title}'.")

    return subreddit


def edit_tracking(tracked_list: list[str]) -> None:

    choice = input(''' | 1 - Add subreddit to tracking list
 | 2 - Remove subreddit from tracking list
 | 3 - Turn back''')
    match choice:
        case "1":
            sub = subreddit_check()
            if sub not in tracked_list:
                database_handler.add_subreddit(sub.lower())
            else:
                print("Already in the tracking list!")

        case "2":
            for count, sub in enumerate(tracked_list):
                print(str(count) + " - " + sub)
            subIndex = int(input(
                "Here's the tracked subreddits list. Please type in the number of the one you no longer want to track: \n")) - 1
            try:
                database_handler.remove_subreddit(
                    tracked_list[subIndex])
            except IndexError:
                print("Not a valid number!")
