from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests

import re
import time
import json

from . import post

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


def get_latest_posts(last_post_id: str, subreddit: str) -> list[post.Post]:
    '''Returns the latest posts up until the last saved post, as a list.'''
    new_posts = []

    for post in posts_list:
        id = post['data']['name']
        if id == last_post_id:
            break

        # fixed reddit class name for post-containers
        container_class = "_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh " + id

        new_post = post.Post(container_class, subreddit)
        new_posts.append(new_post)

    return new_posts
