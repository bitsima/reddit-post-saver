from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests

import re
import time
import json
import logging

from logging_config import logging_config

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)

soup = ""
posts_list = []


def get_main_page(subreddit_name: str) -> int:
    '''Sets the given subreddits main page html data as a global variable.'''

    global soup
    global posts_list

    user_agent = UserAgent()  # instantiating UserAgent seed

    post = None
    while post == None:
        the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

        headers = {
            'User-agent': the_user_agent
        }

        url = f"https://www.reddit.com/r/{subreddit_name}/new/"

        # json data is used to retrieve author names of the posts and getting latest posts
        url_2 = f"https://www.reddit.com/r/{subreddit_name}/new/.json"

        # getting the json data of the main page
        response = requests.get(url_2, headers=headers)

        # making sure subreddit name is true
        if response.status_code != 200:
            return 1

        json_data = response.text
        # getting the html data of the main page
        html_text = requests.get(url, headers=headers).text

        posts_list = json.loads(json_data)['data']['children']
        soup = BeautifulSoup(html_text, "lxml")

        # checking if we can parse the latest post from the page using regex
        post = soup.find("div", class_=re.compile(
            r'^_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh.+'))

        time.sleep(0.2)
    # logging
    logger.info(
        f"Retrieved main page of subreddit '{subreddit_name}' with user agent '{the_user_agent}'.")
    return 0


def get_latest_posts(last_post_id: str, subreddit: str) -> list:
    '''Returns the latest posts up until the last saved post, as a list.'''
    new_posts = []

    for post in posts_list:
        id = post['data']['name']
        if id == last_post_id:
            break

        try:
            new_post = Post(id, subreddit)
        except AttributeError as error:
            logger.error(f"Attribute error occurred: {error}")
            break
        new_posts.append(new_post)

    # logging
    logger.info(f"Parsed '{len(new_posts)}' new posts.")

    return new_posts


def get_last_post(subreddit: str):
    '''Returns the newest post in the subreddit as a Post instance.'''
    id = posts_list[0]['data']['name']

    new_post = Post(id, subreddit)

    return new_post


class Post:
    def __init__(self, id: str, subreddit: str):
        self.subreddit = subreddit
        self.post_id = id
        self.upvotes = self.get_upvotes(id)
        self.time_posted = self.get_time_posted(id)
        self.author = self.get_author(id)
        self.title = self.get_title(id)
        self.content = self.get_content(id)

    @classmethod
    def get_content(self, id: str) -> str:
        '''Returns the text description as a string.'''
        post_content = self.get_post_instance(id).find(
            "div", class_="STit0dLageRsa2yR4te_b")
        try:
            # support for text
            content = ""
            parent = post_content.find(
                "div", class_="_292iotee39Lmt0MkQZ2hPV RichTextJSON-root")
            paragraphs = parent.find_all("p", class_="_1qeIAgB0cPwnLhDF9XSiJM")
            for par in paragraphs:
                content += par.text
        except AttributeError:
            content = "Not supported type of post."
        return content

    @classmethod
    def get_title(self, id: str) -> str:
        '''Returns the title of the post.'''
        post = self.get_post_instance(id)

        title = post.find("h3", class_="_eYtD2XCVieq6emjKBH3m").text

        return title

    @classmethod
    def get_author(self, id: str) -> str:
        '''Returns the author of the post.'''
        post = self.get_post_instance(id)

        author = ""

        for post in posts_list:
            id_ = post['data']['name']
            if id_ == id:
                author = post['data']['author']
                break

        return author

    @classmethod
    def get_time_posted(self, id: str) -> str:
        '''Returns the timestamp of the moment the post was uploaded.'''

        for post in posts_list:
            id_ = post['data']['name']
            if id_ == id:
                time = post['data']['created_utc']
                break

        return time

    @classmethod
    def get_upvotes(self, id: str) -> str:
        '''Returns the given posts upvote count as a string.'''
        post = self.get_post_instance(id)

        upvotes = post.find(
            "div", class_="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo").text

        return upvotes

    @classmethod
    def get_post_instance(self, id: str):

        post = soup.find("div", id=id)

        return post
