'''
Utilizes the Reddit API through functions dealing with the searching for and formatting posts for our
purposes.

Functions:

subreddit_search(reddit: praw.Reddit) -> praw.Reddit.Subreddit
get_subreddit_from_name(reddit: praw.Reddit, name: str) -> praw.Reddit.Subreddit
fetch_new_posts(subreddit: praw.Reddit.Subreddit) -> None
print_posts(submission: praw.Reddit.Submission) -> None

'''

import logging
import praw
from logging_config import logging_config

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)


def subreddit_search(reddit: praw.Reddit) -> praw.Reddit.Subreddit:
    '''Performs a search operation using the Reddit object for a specific Subreddit.'''
    subreddit = input(
        "Please provide a keyword for the subreddit you want to search for: ")

    # logging
    logger.info(f"Started search for subreddit named '{subreddit}'.")

    subreddits = reddit.subreddits.search_by_name(subreddit)
    subreddits_dict = dict()

    counter = 0
    for sub in subreddits:
        counter += 1
        subreddits_dict[counter] = sub
        print(f"{counter} - {sub}")

    number = int(
        input("Please choose the subreddit from the list (Enter a number): "))

    subreddit = reddit.subreddit(subreddits_dict[number].title)

    # logging
    logger.info(f"Chosen subreddit '{subreddit.title}'.")

    return subreddit


def get_subreddit_from_name(reddit: praw.Reddit, name: str) -> praw.Reddit.Subreddit:
    '''Obtain the Subreddit instance with the exact given title.'''
    subreddit = reddit.subreddit(name)
    return subreddit


def fetch_new_posts(subreddit: praw.Reddit.Subreddit) -> None:
    '''Prints out the last 10 posts in the given subreddit, using a specific format.'''
    posts = subreddit.new(limit=10)
    for post in posts:
        print_posts(post)

    # logging
    logger.info(
        f"Fetched and printed last 10 posts from subreddit '{subreddit.title}'.")


def print_posts(submission: praw.Reddit.Submission) -> None:
    '''Prints the given Submission object's data to the terminal in a human-readable format.'''
    print("-----------------------------------\n")
    print(
        f"      Post by {submission.author.name}        Created UTC {submission.created_utc}\n")
    print(submission.title + f"\n{submission.selftext}\n")
    print(f"Upvotes:{submission.score}")
