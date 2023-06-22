
import logging
import database_handling
from src.realtime_crawling import threader
import threading
from src.api_integration import subreddit_handler
from src.realtime_crawling import threader
import praw

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

handler.setFormatter(formatter)

logger.addHandler(handler)


def main():
    logger.info("Program started.")
    database_handling.create_db()

    reddit = praw.Reddit("account")
    # bunu kullanarak real time track etmek lazım
    tracked_subreddits = database_handling.get_subreddits_list()

    print("Hi!")
    choice = input("Please choose the action you desire (Enter a number):\n1 - Add a subreddit to the tracking list\n2 - Remove a subreddit from the tracking list\n3 - Delete saved posts from a specific subreddit\n4 - Show the subreddits in the tracking list\n5 - Show the last 10 posts from a subreddit\n6 - Show the last 10 posts from a subreddit in the tracking list\n")
    match choice:
        case "1":
            sub = subreddit_handler.subreddit_search(reddit).title
            if sub not in tracked_subreddits:
                tracked_subreddits.append(sub.lower())
                database_handling.add_subreddit(sub.lower())
            else:
                print("Already in the tracking list!")
        case "2":
            for sub in tracked_subreddits:
                print(sub)
            sub = input(
                "Here's the tracked subreddits list. Please type in the name of the one you no longer want to track: ")
            if sub in tracked_subreddits:
                tracked_subreddits.remove(sub)
            else:
                print("Not in the list!")
        case "3":
            sub = input(
                "Please enter the name of the subreddit you want its posts deleted from the database: ")
            answer = input(
                f"Do you really want to delete all posts from subreddit {sub}? (y/n)")
            if answer == "y":
                database_handling.remove_subreddit(sub)
                database_handling.remove_from_db(sub)
        case "4":
            print("Here's the tracked subreddits list:")
            for sub in tracked_subreddits:
                print(sub)
        case "5":
            sub = subreddit_handler.subreddit_search(reddit)
            subreddit_handler.fetch_new_posts(sub)
        case "6":
            for sub in tracked_subreddits:
                print(sub)
            answer = input(
                "Here's the tracked subreddits list. Please type in the name of the one you want to see the last 10 saved posts of: ")
            if answer in tracked_subreddits:
                database_handling.print_posts_from_subreddit(answer)
        case _:
            print("Not a valid choice!")


if __name__ == "__main__":
    main()
