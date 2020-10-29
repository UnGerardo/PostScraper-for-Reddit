import praw
import tkinter as tk
from tkinter import ttk
import os
import api_keys as key
import webbrowser


# Takes you to the website the link points to
def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


# Adds a key word to the key word list
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

    # gets the amount of posts the user wants to collect - 'None'/Null (if empty) it gets as many as possible
    num_of_posts = num_of_posts_edit_txt.get("1.0", 'end-1c')
    num_of_posts = num_of_posts.lower()
    if not num_of_posts or num_of_posts == "none" or num_of_posts == "null":
        num_of_posts = None
    else:
        num_of_posts = int(num_of_posts)

    # gets new posts in each sub and searches for keywords in the titles
    # THING TO FIX: if a post title has multiple 'keywords' in it's title it will be shown multiple times
    # THING TO CHECK: some seemingly random posts are appearing, print out keyword found next to title to check
    try:
        for sub in subscribed:
            for post in reddit.subreddit(sub.title).new(limit=num_of_posts):
                for word in key_word_list:
                    if word in post.title.lower():
                        tk.Label(scrollable_frame, text=post.title, bg='#1c2b2d', fg="#5fcfcf",
                                 font='10', justify='center', wraplength=1370).pack()
                        # tk.Label(scrollable_frame, text=word, bg='white').pack()
                        post_link = tk.Label(scrollable_frame, text="https://www.reddit.com" + post.permalink,
                                             bg='#1c2b2d', fg="#99a8b2", cursor="hand2")
                        post_link.pack()
                        post_link.bind("<Button-1>", callback)
                        break
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
    root.configure(bg='#99a8b2')

    # text to label key word input
    add_key_word_txt = tk.Label(root, text='Add a New Key Word:', font='8', bg='#99a8b2', anchor='nw')
    add_key_word_txt.pack()
    add_key_word_txt.place(relx=0.04, rely=0.04)
    new_key_word_txt = tk.Text(root, width=20, height=1)  # creates text box to write in
    new_key_word_txt.pack()  # displays text box
    new_key_word_txt.place(relx=0.16, rely=0.0425)
    add_key_word_btn = tk.Button(root, text='Add Key Word', padx=10,  # create button to add key words
                                 pady=5, fg='black', bg='#e6d5b8', command=add_key_words)
    add_key_word_btn.pack()  # attach button to root but its not attached to the canvas or frame
    add_key_word_btn.place(relx=0.3, rely=0.033)

    amount_of_posts_txt = tk.Label(root, text='Amount of Posts to get:', font='8', bg='#99a8b2', anchor='n')
    amount_of_posts_txt.pack()
    amount_of_posts_txt.place(relx=0.5, rely=0.04)
    num_of_posts_edit_txt = tk.Text(root, width=20, height=1)
    num_of_posts_edit_txt.pack()
    num_of_posts_edit_txt.place(relx=0.63, rely=0.0425)
    get_posts_btn = tk.Button(root, text='Get Posts', padx=10,  # create button to get posts
                              pady=5, fg='black', bg='#e6d5b8', command=get_posts)
    get_posts_btn.pack()  # attach button to root but its not attached to the canvas or frame
    get_posts_btn.place(relx=0.77, rely=0.033)

    # this is the container that holds everything - Extra:allows you to frame widgets bg='#16697A'
    container = tk.Frame(root)
    # drawable canvas behind scrollable frame
    canvas = tk.Canvas(container, bg="#1c2b2d", height=665, width=1345)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    # this is the frame of the entire view where the titles and links are posted, in front of canvas
    scrollable_frame = tk.Frame(canvas, bg="#1c2b2d", height=665, width=1345)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # this allows the scrollable_frame to appear in the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="center")

    # set 'highlightbackground' to the background color of the container because it gets rid of the white outline
    canvas.configure(yscrollcommand=scrollbar.set, highlightbackground='#1c2b2d')

    container.pack()
    container.place(relx=0, rely=0.1)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # runs the gui
    root.mainloop()

    # checks text in save file, if it is different, update it
    with open('Key_Words.txt', 'w+') as file:
        if ','.join(key_word_list) != file.read():
            file.write(','.join(key_word_list))