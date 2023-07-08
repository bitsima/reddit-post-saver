from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests

import re
import time

soup = ""


def get_main_page(subreddit_name: str) -> None:
    '''Sets the given subreddits main page html data as a global variable.'''

    global soup

    user_agent = UserAgent()  # instantiating UserAgent seed

    post = None
    while post == None:
        the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

        url = f"https://www.reddit.com/r/{subreddit_name}/new/"

        headers = {
            'User-agent': the_user_agent
        }

        # getting the html data of the main page
        html_text = requests.get(url, headers=headers).text

        soup = BeautifulSoup(html_text, "lxml")

        # checking if we can parse the latest post from the page using regex
        post = soup.find("div", class_=re.compile(
            r'^_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh.+'))

        time.sleep(1)

    f = open("html_text.html", "w")
    f.write(html_text)
    f.close()


def get_latest_posts(last_post_id: str):
    '''Returns the latest posts up until the last saved post, as a list.'''

    # while post_id != last_post_id:


def get_upvotes(post_container_class: str) -> str:
    '''Returns the given posts upvote count as a string.'''
    post = soup.find("div", class_=post_container_class)

    upvotes = post.find(
        "div", class_="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo").text

    return upvotes


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


def get_author(post_container_class: str) -> str:
    '''Returns the author of the post.'''
    post = soup.find("div", class_=post_container_class)

    author = post.find(
        "a", class_="_2tbHP6ZydRpjI44J3syuqC  _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE").get_text()

    return author


def get_title(post_container_class: str) -> str:
    '''Returns the title of the post.'''
    post = soup.find("div", class_=post_container_class)

    title = post.find("h3", class_="_eYtD2XCVieq6emjKBH3m").text

    return title


def get_content(post_container_class: str) -> str:
    '''Returns the text description as a string.'''
    post_content = soup.find("div", class_=post_container_class).find(
        "div", class_="STit0dLageRsa2yR4te_b")

    # support for text
    content = ""
    parent = post_content.find(
        "div", class_="_292iotee39Lmt0MkQZ2hPV RichTextJSON-root")
    paragraphs = parent.find_all("p", class_="_1qeIAgB0cPwnLhDF9XSiJM")
    for par in paragraphs:
        content += par.text
    return content


class Post:
    def __init__(self, container_class: str):
        self.container_class = container_class
        self.post_id = container_class.split(" ")[-1].strip()
        self.upvotes = get_upvotes(container_class)
        self.time_posted = get_time_posted(container_class)
#        self.author = get_author(container_class)
        self.title = get_title(container_class)
        self.content = get_content(container_class)


post_container_class = re.compile(
    r'^_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh.+')

get_main_page("projectzomboid")

newpost = Post(post_container_class)

print("postID: " + newpost.post_id)
print("upvotes: " + newpost.upvotes)
print("time_posted: " + newpost.time_posted)
# print("author: " + newpost.author)
print("title: " + newpost.title)
print("content: " + newpost.content)
