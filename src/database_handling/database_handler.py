

import sqlite3
import logging

logger = logging.getLogger(__name__)


def create_db():

    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subreddit TEXT
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
        logger.info("Created tables 'posts' and 'subreddits' in the database")
    else:
        logger.info("Tables 'posts' and 'subreddits' already present.")

    conn.commit()
    conn.close()


def add_to_db(submission):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO posts (subreddit, title, author, content, posting_date, up_count, upvote_ratio) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (submission.subreddit.name, submission.title, submission.author, submission.selftext, submission.created_utc, submission.score, submission.upvote_ratio))
    # logging
    logger.info(
        f"Added new post by '{submission.author}' in subreddit '{submission.subreddit.name}' to the database")

    conn.commit()
    conn.close()


def add_subreddit(name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO subreddits (subreddit) VALUES (?)", (name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(f"Added new subreddit '{name}' to the subreddit table")


def remove_subreddit(name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subreddits WHERE subreddit = ?", (name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(f"Removed subreddit '{name}' from the subreddits table")


def remove_from_db(subreddit_name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE subreddit = ?", (subreddit_name,))

    conn.commit()
    conn.close()

    # logging
    logger.info(
        f"Deleted all saved posts from the subreddit '{subreddit_name}' from the posts table")


def get_subreddits_list():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subreddits")
    subreddits = cursor.fetchall()

    # logging
    logger.info("Fetched the tracked subreddits list from the subreddits table")

    return subreddits


def print_posts_from_subreddit_db(name):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE subreddit = ?", (name,))
    rows = cursor.fetchall()

    ##### buraya ayar çekmek lazım #########
    for col in rows[:10]:
        print(col)

    # logging
    logger.info(f"Printed last 10 saved posts from the subreddit '{name}'")
