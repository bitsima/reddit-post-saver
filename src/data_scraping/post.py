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
