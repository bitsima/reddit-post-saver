import logging
import os

from database_handling import database_handler
from data_scraping import scraper
from logging_config import logging_config

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)


def interact() -> None:

    # keeping the tracked subreddit list up to date with the database
    tracked_subreddits = database_handler.get_subreddits_list()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    print(''' | 1 - See the tracking list
 | 2 - Edit the tracking list
 | 3 - See saved posts''')
    choice = input("What would you like to do? Please enter a number: \n")
    os.system("clear")
    match choice:
        case "1":  # See the tracking list
            if len(tracked_subreddits) == 0:
                print("\nTracked subreddits list seems to be empty :(")
                return

            print("\nHere's the tracked subreddits list:")
            for count, sub in enumerate(tracked_subreddits):
                print(str(count + 1) + " - " + sub)

        case "2":  # Edit the tracking list
            edit_tracking(tracked_subreddits)

        case "3":  # See saved posts'
            if len(tracked_subreddits) == 0:
                print(
                    "\nPlease add some subreddits to the tracking list first >:(")
                return
            for count, sub in enumerate(tracked_subreddits):
                print(str(count + 1) + " - " + sub)

            subIndex = int(input(
                "Here's the tracked subreddits list. Please enter the number of the one you want to see the last 10 saved posts of: \n")) - 1
            try:
                sub = tracked_subreddits[subIndex]
            except IndexError:
                print("Not a valid number!")
            database_handler.print_posts_from_subreddit_db(sub)

        case _:
            "Not a valid choice!"


def subreddit_check() -> str:
    '''Checks if the given subreddit name is true.'''
    subreddit = input(
        "Please provide the name of the subreddit you want to search for:\n")
    print("\nPlease wait...")
    # logging
    logger.info(f"Started search for subreddit named '{subreddit}'.")

    error_occurred = scraper.get_main_page(subreddit)

    if error_occurred:
        print("That's not a valid subreddit name!")
        return
    else:
        print(f"'{subreddit}' was added to the tracking list successfully!")
    # logging
    logger.info(f"Chosen subreddit '{subreddit.title}'.")

    return subreddit


def edit_tracking(tracked_list: list[str]) -> None:

    choice = input('''\n | 1 - Add subreddit to tracking list
 | 2 - Remove subreddit from tracking list
 | 3 - Turn back
What would you like to do? Please enter a number: \n''')
    match choice:
        case "1":
            sub = subreddit_check()
            if sub not in tracked_list:
                database_handler.add_subreddit(sub.lower())
            else:
                print("Already in the tracking list!")

        case "2":
            if len(tracked_list) == 0:
                print("\nTracked subreddits list seems to be empty :(")
                return

            for count, sub in enumerate(tracked_list):
                print(str(count + 1) + " - " + sub)
            subIndex = int(input(
                "Here's the tracked subreddits list. Please type in the number of the one you no longer want to track: \n")) - 1
            try:
                database_handler.remove_subreddit(
                    tracked_list[subIndex])
            except IndexError:
                print("Not a valid number!")
