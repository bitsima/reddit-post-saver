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


def get_main_page(subreddit_name: str) -> None:
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
        json_data = requests.get(url_2, headers=headers).text

        # getting the html data of the main page
        html_text = requests.get(url, headers=headers).text

        posts_list = json.loads(json_data)['data']['children']
        soup = BeautifulSoup(html_text, "lxml")

        # checking if we can parse the latest post from the page using regex
        post = soup.find("div", class_=re.compile(
            r'^_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh.+'))

        time.sleep(1)

    # logging
    logger.info(
        f"Retrieved main page of subreddit '{subreddit_name}' with user agent '{the_user_agent}'.")


def get_latest_posts(last_post_id: str, subreddit: str) -> list[Post]:
    '''Returns the latest posts up until the last saved post, as a list.'''
    new_posts = []

    for post in posts_list:
        id = post['data']['name']
        if id == last_post_id:
            break

        # fixed reddit class name for post-containers
        container_class = "_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh " + id

        new_post = Post(container_class, subreddit)
        new_posts.append(new_post)

    # logging
    logger.info(f"Parsed '{len(new_posts)}' new posts.")

    return new_posts


class Post:
    def __init__(self, container_class: str, subreddit: str):
        self.subreddit = subreddit
        self.container_class = container_class
        self.post_id = container_class.split(" ")[-1].strip()
        self.upvotes = self.get_upvotes(container_class)
        self.time_posted = self.get_time_posted(container_class)
        self.author = self.get_author(container_class, subreddit)
        self.title = self.get_title(container_class)
        self.content = self.get_content(container_class)

    @classmethod
    def get_content(post_container_class: str) -> str:
        '''Returns the text description as a string.'''
        post_content = soup.find("div", class_=post_container_class).find(
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
    def get_title(post_container_class: str) -> str:
        '''Returns the title of the post.'''
        post = soup.find("div", class_=post_container_class)

        title = post.find("h3", class_="_eYtD2XCVieq6emjKBH3m").text

        return title

    @classmethod
    def get_author(post_container_class: str) -> str:
        '''Returns the author of the post.'''
        post = soup.find("div", class_=post_container_class)

        post_id = post_container_class.split(' ')[-1].strip()

        author = ""

        for post in posts_list:
            id = post['data']['name']
            if id == post_id:
                author = post['data']['author']
                break

        return author

    @classmethod
    def get_time_posted(post_container_class: str) -> str:
        '''Returns the timestamp of the moment the post was uploaded.'''
        post = soup.find("div", class_=post_container_class)

        time_ = post.find("span", class_="_2VF2J19pUIMSLJFky-7PEI").text

        temp_list = time_.split(" ")

        time_posted = time_
        if temp_list[1] == "second" or temp_list[1] == "seconds":
            time_posted = time.time() - int(temp_list[0])
            time_posted = str(int(time_posted))
        elif temp_list[1] == "minute" or temp_list[1] == "minutes":
            time_posted = time.time() - int(temp_list[0])*60
            time_posted = str(int(time_posted))
        # other cases not needed
        return time_posted

    @classmethod
    def get_upvotes(post_container_class: str) -> str:
        '''Returns the given posts upvote count as a string.'''
        post = soup.find("div", class_=post_container_class)

        upvotes = post.find(
            "div", class_="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo").text

        return upvotes
