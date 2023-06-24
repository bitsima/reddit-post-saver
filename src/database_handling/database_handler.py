'''
Handle all the interactions with the database using its functions on creation, addition,
removal, etc.

Functions:

create_db() -> None
add_to_db(submission: praw.Reddit.Submission) -> None
add_subreddit(name: str) -> None
remove_subreddit(name: str) -> None
remove_posts(subreddit_name: str) -> None
get_subreddits_list() -> list[str]
get_latest_post_id(name: str) -> str
print_posts_from_subreddit_db(name: str) -> None

'''
import sqlite3
import logging
import praw
from logging_config import logging_config

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)


def create_db() -> None:
    '''Create the database if not already exists with the keys: postID, subreddit, title,
    author, content, posting_date, up_count, down_count, upvote_ratio.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            postID TEXT PRIMARY KEY ,
            subreddit TEXT,
            title TEXT,
            author TEXT,
            content TEXT,
            posting_date TEXT,
            up_count INTEGER,
            down_count INTEGER,
            upvote_ratio REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subreddits (
            subreddit TEXT PRIMARY KEY
        )
    ''')

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", ("posts",))
    exists = cursor.fetchone()

    if not exists:
        # logging
        logger.info("Created tables 'posts' and 'subreddits' in the database.")
    else:
        logger.info("Tables 'posts' and 'subreddits' already present.")

    conn.commit()
    conn.close()


def add_to_db(submission: praw.Reddit.Submission) -> None:
    '''Adds a new post to the database after extracting the wanted data from the Submission instance.'''
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO posts (postID, subreddit, title, author, content, posting_date, up_count, upvote_ratio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (submission.id, submission.subreddit.display_name, submission.title, submission.author.name, submission.selftext, submission.created_utc, submission.score, submission.upvote_ratio))
    # logging
    logger.info(
        f"Added new post by '{submission.author}' in subreddit '{submission.subreddit.name}' to the database.")

    conn.commit()
    conn.close()


def add_subreddit(name: str) -> None:
    '''Adds a new subreddit to the 'subreddits' table in the database.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO subreddits (subreddit) VALUES (?)", (name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(f"Added new subreddit '{name}' to the 'subreddit' table.")


def remove_subreddit(name: str) -> None:
    '''Removes the subreddit with the given name from the 'subreddits' table in the database.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subreddits WHERE subreddit = ?", (name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(f"Removed subreddit '{name}' from the 'subreddits' table.")


def remove_posts(subreddit_name: str) -> None:
    '''Removes all posts in the database where their subreddit name == subreddit_name.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE subreddit = ?", (subreddit_name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(
        f"Deleted all saved posts from the subreddit '{subreddit_name}' from the 'posts' table.")


def get_subreddits_list() -> list[str]:
    '''Returns the subreddits' names that are tracked and currently kept in the database.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT subreddit FROM subreddits")
    subreddits = cursor.fetchall()
    # subreddits was in the form [('abc',), ('cde',)]
    subreddits = ["".join(x) for x in subreddits]

    # logging
    logger.info("Fetched the tracked subreddits list from the subreddits table.")

    return subreddits


def get_latest_post_id(name: str) -> str:
    '''Returns the last added posts id.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT postID FROM posts WHERE subreddit = ? ORDER BY posting_date DESC", (name,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        return "0"

    # logging
    logger.info(f"Fetched latest post for the subreddit '{name}'.")

    return list(rows[0])[0]


def print_posts_from_subreddit_db(name: str) -> None:
    '''Prints the last 10 saved posts' kept data to the terminal, in a human-readable format.'''

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE subreddit = ?", (name,))
    rows = cursor.fetchall()
    '''rows = [('postID', 'subreddit', 'title', 'author', 'content',
                'posting_date', 'up_count', 'down_count', 'upvote_ratio'),]'''

    for row in rows[:10]:
        print(f"""postID: {row[0]}    in subreddit: {row[1]}  by author: {row[3]} posted on UTC: {row[5]}
            {row[2]}
            {row[4]}
            up_count: {row[6]}""")

    # logging
    logger.info(f"Printed last 10 saved posts from the subreddit '{name}'.")
