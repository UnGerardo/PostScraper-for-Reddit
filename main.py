import praw
import tkinter as tk
from tkinter import ttk
import os
import api_keys as key
import webbrowser


# Takes you to the website the link points to
def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


# Adds a key word to the skey word list
def add_key_words():
    # this gets the text input in the text box
    key_word = new_key_word_txt.get("1.0", 'end-1c')
    # if the text isn't empty add it to the key word list
    if key_word:
        key_word_list.append(key_word)


# Gets posts from reddit and prints them out
def get_posts():
    # clears the frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # gets new posts in each sub and searches for keywords in the titles
    # THING TO FIX: if a post title has multiple 'keywords' in it's title it will be shown multiple times
    # THING TO CHECK: some seemingly random posts are appearing, print out keyword found next to title to check
    try:
        for sub in subscribed:
            for post in reddit.subreddit(sub.title).new(limit=50):
                for word in key_word_list:
                    if word in post.title.lower():
                        tk.Label(scrollable_frame, text=post.title, bg='white').pack()
                        post_link = tk.Label(scrollable_frame, text="https://www.reddit.com" + post.permalink, bg='white', fg="blue", cursor="hand2")
                        post_link.pack()
                        post_link.bind("<Button-1>", callback)
                        # print(post.title, "https://www.reddit.com" + post.permalink)
    except:
        print('Ran into an error getting posts')


if __name__ == '__main__':

    key_word_list = []

    # creates new save text file if it doesn't exist
    if not os.path.isfile('Key_Words.txt'):
        with open('Key_Words.txt', 'w') as file:
            file.write('')
    else:  # if it does exist copy its strings into key_word_list and split by the commas
        with open('Key_Words.txt', 'r') as file:
            fileContent = file.read()
            key_word_list = fileContent.split(',')

    # authentication
    reddit = praw.Reddit(client_id=key.MY_CLIENT_ID, client_secret=key.MY_CLIENT_SECRET,
                         user_agent=key.MY_USER_AGENT, username=key.MY_USERNAME,
                         password=key.MY_PASSWORD)

    # get subreddits the user follows
    subscribed = list(reddit.user.subreddits(limit=None))

    # root is the body of the gui, name needs space as first char because it goes lowercase
    root = tk.Tk(className=' Post Scrapper')
    # sets the window size at the size inside 'widthxheight'
    root.geometry("500x500")

    # text to label key word input
    add_key_word_txt = tk.Label(root, text='Add a New Key Word')
    add_key_word_txt.pack()
    add_key_word_txt.place(relx=0.1, rely=0.05)
    new_key_word_txt = tk.Text(root, width=20, height=1)  # creates text box to write in
    new_key_word_txt.pack()  # displays text box
    new_key_word_txt.place(relx=0.2, rely=0.05)
    add_key_word_btn = tk.Button(root, text='Add Key Word', padx=10,  # create button to add key words
                                 pady=5, fg='white', bg='#DB6400', command=add_key_words)
    add_key_word_btn.pack()  # attach button to root but its not attached to the canvas or frame
    add_key_word_btn.place(relx=0.35, rely=0.05)

    get_posts_btn = tk.Button(root, text='Get Posts', padx=10,  # create button to get posts
                              pady=5, fg='white', bg='#DB6400', command=get_posts)
    get_posts_btn.pack()  # attach button to root but its not attached to the canvas or frame
    get_posts_btn.place(relx=0.45, rely=0.05)

    # allows you to frame widgets bg='#16697A'
    container = tk.Frame(root, height="500", width="1500", bg="yellow")
    canvas = tk.Canvas(container, bg="blue", height=590, width=1345)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    # this is the frame of the entire view where the titles and links are posted
    scrollable_frame = tk.Frame(canvas, bg="#16697A")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    container.pack()
    container.place(relx=0, rely=0.2)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # runs the gui
    root.mainloop()

    # checks text in save file, if it is different, update it
    with open('Key_Words.txt', 'w+') as file:
        if ','.join(key_word_list) != file.read():
            file.write(','.join(key_word_list))