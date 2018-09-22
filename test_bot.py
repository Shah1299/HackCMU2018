#from flask import Flask, request, redirect, url_for, render_template, session, g, flash, jsonify
import praw
from tkinter import *
from tkinter.font import Font
import os
import sys
import subprocess
import traceback

#app = Flask(__name__)

#------------------------------------------
#All the PRAW stuff

def bot_login():
        '''reddit = praw.Reddit(client_id = "W1d0uZ96JxlhOQ",
                            client_secret = "Z2DAIwamfcAmHDjW9N0FZ7k-guQ",
                            username = "HackCMU_Bot",
                            password = "HackCMU_Bot",
                            user_agent = "HackCMU_Bot by HackCMU students")'''
        
        reddit = praw.Reddit(client_id = "EwKpTDHxLQWiOg",
                            client_secret = "QvQ4qFuM7-7-IP2aWyFZqixg2cs",
                            username = "CMU_Meme_Bot",
                            password = "CMU_Meme_Bot",
                            user_agent = "CMU_Meme_Bot by HackCMU 2018 students")
        return reddit
    
reddit = bot_login()
'''
def print_subreddit_top_5(r, sub_name):
    subreddit = r.subreddit("funny")
    print("Subreddit: " + subreddit.display_name)
    print ("")
    #print(subreddit.description)

    posts = subreddit.hot(limit=5)
    i = 0
    for submission in posts:
        if not submission.stickied:
            i += 1
            print ("Submission " + str(i) + ":")
            print ("Title: " + submission.title)
            print("")
            print ("Top 5 comments: ")
            submission.comments.replace_more(limit=5)
            c = 0
            for comment in submission.comments.list():
                print("Comment " + str(c + 1) + ": " + comment.body)
                c += 1
                if (c >= 5):
                    break
            print("")
    print ("TOP POSTS SUCCESSFULLY ACQUIRED.")

PAY_RESPECTS_VARIANTS = ["pay respects", "press f ", "rest in peace", "testing"]
def pay_respects_test (r, sub_name):
    subreddit = r.subreddit(sub_name)
    print("Pay respects on subreddit: " + subreddit.display_name)
    print ("")
    posts = subreddit.new(limit=25) #shouldn't be more than this many new posts per minute
    for submission in posts:
        if (submission.stickied):
            continue
        for s in PAY_RESPECTS_VARIANTS:
            if (submission.title.lower().find(s) != -1):
                submission.reply("Good job testing.")
            for comment in submission.comments.list(): #only top level comments
                try:     
                    if (comment.body.lower().find(s) != -1):
                        comment.reply("Good job testing, and a good reply.")
                except:
                    continue

#pay_respects_test (reddit, "test")
    
''' 
    
#returns a flat list of all comments
def fetch_all_comments(submission):
    all_comments = []
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        get_replies(all_comments, top_level_comment)
    return all_comments
        
#recursively populates li parameter with all replies
def get_replies(li, top_comment):
    li.append(top_comment)
    for comment in top_comment.replies:
        get_replies(li, comment)

MPAA_RATING_NAMES = {}
MPAA_RATING_NAMES[0] = "G"
MPAA_RATING_NAMES[1] = "PG"
MPAA_RATING_NAMES[2] = "PG-13"
MPAA_RATING_NAMES[3] = "R"

R_WORDS = ["clitoris", "fellate", "fellatio", "fuck", "labia", "nigger", "nigga", "penis"]
PG_13_WORDS = ["anal", "anus", "arse", "ass", "ballsack", "bastard", "bitch", "biatch", "bloody", "blowjob", "blow job", "bollock", "bollok", "boner", "boob", "bugger", "bum",  "buttplug", "cock", "coon", "cunt", "damn", "dick", "dildo", "dyke", "fag", "feck",  "felching", "flange", "Goddamn", "God damn", "hell", "homo", "jizz", "knobend", "knob end",  "lmao", "lmfao", "muff", "piss", "prick", "pube", "pussy", "queer", "scrotum", "sex", "shit", "s hit", "sh1t", "slut", "smegma", "spunk", "tosser", "twat", "vagina", "wank", "whore", "wtf"]
PG_WORDS = ["butt", "fudgepacker", "fudge packer", "crap", "darn", "jerk", "heck", "poop", "turd"]

SPACE_BEFORE_CHECK_WORDS = ["anal", "anus", "arse", "ass", "hell", "jerk", "crap"]
SPACE_AFTER_CHECK_WORDS = ["butt", "turd"]


def get_thread_mpaa_rating (submission):
    to_return = []
    to_return.append ("Post Title: " + submission.title)
    to_return.append ("Post Score: " + str(submission.score))
    comments_objects_list = fetch_all_comments(submission)
    comments_list = []
    for comment in comments_objects_list:
        try:
            comments_list.append(comment.body)
        except:
            continue

    to_return.append("Number of Comments: " + str(len(comments_list)))
    try:
        comments_list.append(submission.title)
        comments_list.append(submission.selftext)
    except:
        pass
    r_counts = {}
    pg_13_counts = {}
    pg_counts = {}
    
    for rw in R_WORDS:
        r_counts[rw] = 0
    for pg13w in PG_13_WORDS:
        pg_13_counts[pg13w] = 0
    for pgw in PG_WORDS:
        pg_counts[pgw] = 0
    
    word_counts = [r_counts, pg_13_counts, pg_counts]
    
    rating = 3
    
    rating_explanation = []
    for comment_text in comments_list:
        for count_dict in word_counts:
            for word in count_dict:
                count = 0
                if (word in SPACE_BEFORE_CHECK_WORDS):
                    count = (" " + comment_text).count(" " + word)
                elif (word in SPACE_AFTER_CHECK_WORDS):
                    count = (comment_text + " ").count(word + " ")
                else:
                    count_dict[word] += comment_text.count(word)
    
    for count_dict in word_counts:
        for word in count_dict:
            if ((word != "fuck" and count_dict[word] > 0) or (word == "fuck" and count_dict[word] > 1)):
                for word in count_dict:
                    if ((word != "fuck" and count_dict[word] > 0) or (word == "fuck" and count_dict[word] > 1)):
                        rating_explanation.append("Post + Comments contains the word: \"" + word + "\" " + str(count_dict[word]) + " times.")
                if (len(rating_explanation) != 0):
                    break
        if (len(rating_explanation) != 0):
            break
        rating -= 1
    if (rating == 0):
        rating_explanation.append ("Post + Comments contains no bad language.")
    mpaa_rating_name = MPAA_RATING_NAMES[rating]
    to_return.append("Post + Comments MPAA Rating: " + mpaa_rating_name)
    to_return.extend(rating_explanation)
    return to_return

def nl_indent_string_list (list):
    string_count = 0
    final = ""
    for s in list:
        if (string_count != 0):
            s = "\n" + s
        final += s
        string_count += 1
    return final

#------------------------------------------
#GUI STUFF:

root = Tk()
root.title("Rated R for Reddit")
root.geometry("800x400")

font_title = Font(family = "Helvetica", size = 20)
font_url = Font(family = "Helvetica", size = 12)
font_rating = Font(family = "Helvetica", size = 14)
font_credit = Font(family = "Helvetica", size = 12)

#root.resizable(width = False, height = False)
prompt = Label(root, text = "Paste in a reddit thread url!\nWe'll give you its MPAA rating (e.g. PG-13).", font=font_title)
prompt.pack()

e = Entry(root, width = 50, font=font_url)
e.pack(padx = 10, pady = 5)
e.focus_set()
e.pack()

rating_string_var = StringVar()
rating_string_var.set("Rating will appear here.")
def show_rating():
    try:
        rating_string_var.set("Determining rating...")
        submission = reddit.submission(url = e.get())
        returned_rating_list = get_thread_mpaa_rating(submission)
        to_print = nl_indent_string_list(returned_rating_list)
        rating_string_var.set(to_print)
        #put this rating in the label below the rate button
    except:
        rating_string_var.set("Error fetching submission data and/or determining rating.")
        print (traceback.format_exc())

b = Button (root, text = "Rate!", width = 10, font=font_title, command = show_rating)
b.pack()

rating_label = Label(root, textvariable = rating_string_var, font=font_rating)
rating_label.pack()

credit_label = Label(root, text = "Made by Shalin Shah and Jenny Fish, for HackCMU 2018.", font = font_credit)
credit_label.pack(side = 'bottom', padx = 5, pady = 5)

root.mainloop()


#------------------------------------------

#wait no this isn't what we want
'''
@app.route('/')
def render_something():
    return "test successful"

@app.route('/<subreddit>/<number>')
def get_mpaa_ratings(subreddit, number):
    return jsonify(get_multiple_mpaa_ratings(subreddit, int(number)))
    


if __name__=='__main__':
    app.run(debug=True,host="127.0.0.1", port=3000)
'''