# reddit-post-saver

This project allows users to search and select subreddits they want to track. In real-time, the script saves new posts from these subreddits to a database using SQLite. The processing of real-time data and user inputs is handled in separate threads for efficient execution.

# Features
 - User-friendly interface for searching and selecting subreddits.
 - Real-time processing of new posts from selected subreddits.
 - Automatic saving of new posts to an SQLite database for easy retrieval.
 - Multithreaded architecture for handling real-time data and user inputs concurrently.
 - Utilizing the Reddit API in order to scrape data.

# Requirements
 - To run this project, just do:

pip install -r requirements.txt

 - You need your own Reddit script app CLIENT_ID and CLIENT_SECRET values placed in the praw.ini file.
Get your own values from here:
https://www.reddit.com/prefs/apps/

 - Then just run the main.py.

# TODO Ideas for the future (maybe):
 - Testing
 - Creating the docker image of the project
 - Proper documentation and docstrings
 - Scheduled backup for the database
 - Saving the comments of the posts in the subreddit
 - Message Queue Processing: Performing operations based on the message content
 - Implementing OAuth 2.0 authentication flow, turning it to a web app and adding the option to log in to reddit as well as to the service
 - Saving old posts from subreddits
 - Improving some functionalities, such as being able to see all of the saved posts
 - More comprehensive logging and being able to see the logs from the app in a given interval
