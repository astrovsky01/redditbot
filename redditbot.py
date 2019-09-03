#!/usr/bin/env python
import argparse
import praw

parser = argparse.ArgumentParser(description='Monitor subreddits for galaxy.')
parser.add_argument("--subreddit", nargs="*", help="Specify which subreddits to monitor")
args = parser.parse_args()
subs = args.subreddit
#reddit api login
r = praw.Reddit(client_id="zXULpqlTt7u5iw", client_secret="*",
               username="galaxyprojectbot", password="*",
               user_agent="galaxyprojectbot from the Galaxy Project")

#trigger word for the bot
keyphrase = "galaxy"

#Comment response
response_string = "**[Galaxy bot]** Galaxy is an open, web-based platform for accessible, reproducible, and transparent computational biomedical research. If you have any questions, visit [our website](https://galaxyproject.org) or our [Gitter channel](https://gitter.im/galaxyproject/Lobby)."

for n in subs:
    #monitored subreddit. Request permissions from mods to add in additional ones.
    subreddit = r.subreddit(n)
    #To ensure the script runs quickly, only look at the last 20 posts
    count = 0
    for submission in subreddit.new():

        count += 1
        commentors = []
        c_on_c = []
        comments = submission.comments
        already_commented = False

        for i in comments:
            replies = i.replies
            if i.author not in commentors:
                commentors.append(i.author)
            for n in replies:
                if n.author not in c_on_c:
                    c_on_c.append(n.author)
        #Found reference to Galaxy in post title
        if (keyphrase in submission.title or keyphrase.title() in submission.title) and (submission.author != "galaxyprojectbot"):
            if ("galaxyprojectbot" not in commentors) and ("galaxyprojectbot" not in c_on_c):
                submission.upvote()
                submission.reply(response_string)
                #print("Due to title, upvoted and responded to " + submission.title)
        #Found reference to Galaxy in post body
        elif (keyphrase in submission.selftext or keyphrase.title() in submission.selftext) and (submission.author != "galaxyprojectbot"):
            if ("galaxyprojectbot" not in commentors) and ("galaxyprojectbot" not in c_on_c):
                submission.upvote()
                submission.reply(response_string)
                #print("Due to submission body, upvoted and responded to " + submission.title)
        #Look for reference to Galaxy in comments, only respond the first time it's mentioned
        elif ("galaxyprojectbot" not in commentors) and ("galaxyprojectbot" not in c_on_c):
            for x in comments:
                if (already_commented == False) and ("galaxyprojectbot" not in commentors) and ("galaxyprojectbot" not in c_on_c):
                    x.upvote()
                    x.reply(response_string)
                    already_commented = True
                    #print("Due to submission comments, upvoted and responded to " + submission.title)
                    continue
        if count >= 20:
            break
