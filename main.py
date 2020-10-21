import praw
import api_keys as key

if __name__ == '__main__':
    # authentication
    reddit = praw.Reddit(client_id=key.MY_CLIENT_ID, client_secret=key.MY_CLIENT_SECRET, user_agent=key.MY_USER_AGENT, username=key.MY_USERNAME, password=key.MY_PASSWORD)

    # get subreddits the user follows
    subscribed = list(reddit.user.subreddits(limit=None))

    # key words need in post titles
    key_words = ['python', 'node', 'javascript', 'c++', 'course', 'tutorial']

    # gets new posts in each sub and searches for keywords in the titles
    for sub in subscribed:
        for post in reddit.subreddit(sub.title).new(limit=10):
            for key_word in key_words:
                if key_word in post.title.lower():
                    print(post.title, "https://www.reddit.com" + post.permalink)