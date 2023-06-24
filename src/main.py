import threading
import logging
import praw
from realtime_crawling import threader
from api_integration import subreddit_handler
from logging_config import logging_config
from database_handling import database_handler


logging_config.configure_logging()
logger = logging.getLogger(__name__)

print("\nHi!")
logger.info("Program started.")

database_handler.create_db()

reddit = praw.Reddit("account")


def main():

    # keeping the tracked subreddit list up to date with the database
    tracked_subreddits = database_handler.get_subreddits_list()
    print("-----------------------------------")
    choice = input("""1 - Add a subreddit to the tracking list
2 - Remove a subreddit from the tracking list
3 - Delete saved posts from a specific subreddit
4 - Show the subreddits in the tracking list
5 - Show the last 10 posts from a subreddit
6 - Show the last saved 10 posts from a subreddit in the tracking list
Please choose the action you desire (Enter a number):\n""")

    match choice:
        case "1":  # Add a subreddit to the tracking list
            sub = subreddit_handler.subreddit_search(reddit).title
            if sub not in tracked_subreddits:
                database_handler.add_subreddit(sub.lower())
            else:
                print("Already in the tracking list!")
        case "2":  # Remove a subreddit from the tracking list
            counter = 0
            for sub in tracked_subreddits:
                counter += 1
                print(str(counter) + " - " + sub)
            subIndex = int(input(
                "Here's the tracked subreddits list. Please type in the number of the one you no longer want to track: ")) - 1
            try:
                database_handler.remove_subreddit(
                    tracked_subreddits[subIndex])
            except IndexError:
                print("Not a valid number!")
        case "3":  # Delete saved posts from a specific subreddit
            counter = 0
            for sub in tracked_subreddits:
                counter += 1
                print(str(counter) + " - " + sub)

            subIndex = int(input(
                "Here's the tracked subreddits list. Please enter the number of the subreddit you want its posts deleted from the database: ")) - 1
            try:
                sub = tracked_subreddits[subIndex]
            except IndexError:
                print("Not a valid number!")
            answer = input(
                f"Do you really want to delete all posts from subreddit {sub}? (y/n)")
            if answer == "y":
                database_handler.remove_subreddit(sub)
                database_handler.remove_posts(sub)
        case "4":  # Show the subreddits in the tracking list
            print("Here's the tracked subreddits list:")
            for sub in tracked_subreddits:
                print(sub)
        case "5":  # Show the last 10 posts from a subreddit
            sub = subreddit_handler.subreddit_search(reddit)
            subreddit_handler.fetch_new_posts(sub)
        case "6":  # Show the last saved 10 posts from a subreddit in the tracking list
            counter = 0
            for sub in tracked_subreddits:
                counter += 1
                print(str(counter) + " - " + sub)

            subIndex = int(input(
                "Here's the tracked subreddits list. Please enter the number of the one you want to see the last 10 saved posts of: ")) - 1
            try:
                sub = tracked_subreddits[subIndex]
            except IndexError:
                print("Not a valid number!")
            if answer in tracked_subreddits:
                database_handler.print_posts_from_subreddit(answer)
        case _:
            print("Not a valid choice!")


if __name__ == "__main__":
    t1 = threading.Thread(target=threader.real_time_check, args=(reddit,))
    t1.start()
    while True:  # we need the checks to run as long as the program is running
        try:
            main()
        except Exception as error:
            print("An error occurred: ", error)

            # logging
            logger.error(f"An error occurred: {error}")
