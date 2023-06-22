import sqlite3
import logging
from logging_config import logging_config

logging_config.configure_logging()
logger = logging.getLogger(__name__)


def create_db():

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


def add_to_db(submission):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO posts (postID, subreddit, title, author, content, posting_date, up_count, upvote_ratio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (submission.id, submission.subreddit.display_name, submission.title, submission.author.name, submission.selftext, submission.created_utc, submission.score, submission.upvote_ratio))
    # logging
    logger.info(
        f"Added new post by '{submission.author}' in subreddit '{submission.subreddit.name}' to the database.")

    conn.commit()
    conn.close()


def add_subreddit(name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO subreddits (subreddit) VALUES (?)", (name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(f"Added new subreddit '{name}' to the subreddit table.")


def remove_subreddit(name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subreddits WHERE subreddit = ?", (name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(f"Removed subreddit '{name}' from the subreddits table.")


def remove_posts(subreddit_name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE subreddit = ?", (subreddit_name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(
        f"Deleted all saved posts from the subreddit '{subreddit_name}' from the posts table.")


def get_subreddits_list():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT subreddit FROM subreddits")
    subreddits = cursor.fetchall()
    subreddits = ["".join(x) for x in subreddits]
    # logging
    logger.info("Fetched the tracked subreddits list from the subreddits table.")

    return subreddits


def get_latest_post_id(name):
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


def print_posts_from_subreddit_db(name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE subreddit = ?", (name,))
    rows = cursor.fetchall()

    for row in rows[:10]:
        for col in row:
            print(col)

    # logging
    logger.info(f"Printed last 10 saved posts from the subreddit '{name}'.")
