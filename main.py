import praw
import tkinter as tk
from tkinter import filedialog, Text
import os
import api_keys as key


def add_key_words(key_word):
    key_word_list.append(key_word)


def get_posts():
    # clears the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # gets new posts in each sub and searches for keywords in the titles
    try:
        for sub in subscribed:
            for post in reddit.subreddit(sub.title).new(limit=10):
                for word in key_word_list:
                    if word in post.title.lower():
                        post_title = tk.Label(frame, text=post.title, bg='gray')
                        post_title.pack()
                        post_url = tk.Label(frame, text="https://www.reddit.com" + post.permalink, bg='gray')
                        post_url.pack()
                        # print(post.title, "https://www.reddit.com" + post.permalink)
    except:
        print('Ran into an error getting posts')


if __name__ == '__main__':

    key_word_list = []

    # authentication
    reddit = praw.Reddit(client_id=key.MY_CLIENT_ID, client_secret=key.MY_CLIENT_SECRET,
                         user_agent=key.MY_USER_AGENT, username=key.MY_USERNAME,
                         password=key.MY_PASSWORD)

    # get subreddits the user follows
    subscribed = list(reddit.user.subreddits(limit=None))
