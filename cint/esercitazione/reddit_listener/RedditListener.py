import praw
import json

def processSubmission(reddit, submission):
    # Check https://praw.readthedocs.io/en/stable/code_overview/models/submission.html to customize
    # what to get from Reddit

    data = {}
    author = {
        "id": submission.author.id,
        "name": submission.author.name,
        "comment_karma": submission.author.comment_karma,
        "is_mod": submission.author.is_mod,
        "is_employee": submission.author.is_employee,
    }
    data["submission"] = {
        "author":author,
        "id": submission.id,
        "created_utc": submission.created_utc,
        "subreddit_name": submission.subreddit_name_prefixed,
        "subreddit_id": submission.subreddit_id,
        "title": submission.title,
        "url": submission.url
    }
    print(json.dumps(data))



def processComment(reddit, comment):
    # Check https://praw.readthedocs.io/en/stable/code_overview/models/comment.html to customize
    # what to get from Reddit

    data = {}
    author = {
        "id": comment.author.id,
        "name": comment.author.name,
        "comment_karma": comment.author.comment_karma,
        "is_mod": comment.author.is_mod,
        "is_employee": comment.author.is_employee,
    }
    data["comment"] = {
        "author": author,
        "body_html": comment.body_html,
        "created_utc": comment.created_utc,
        "parent_id": comment.parent_id,
        "score": comment.score,
        "stickied": comment.stickied,
        "submission_id": comment.submission.id,
        "submission_title": comment.submission.title,
        "subreddit_name": comment.submission.subreddit_name_prefixed,
        "subreddit_id": comment.submission.subreddit_id,
    }
    print(json.dumps(data))

def getStreamedRedditContents(client_id, client_secret, content_type, subreddit):
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='My custom agent')
    reddit.config.store_json_result = True

    if content_type == "submission":
        for submission in reddit.subreddit(subreddit).stream.submissions():
            processSubmission(reddit, submission)
    else:
        for comment in reddit.subreddit(subreddit).stream.comments():
            processComment(reddit, comment)
            


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Reddit listener using PRAW library",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("client_id", help="The client ID of the app registered on dev part of Reddit")
    parser.add_argument("secret_key", help="The secret key of the app specified by client ID")
    parser.add_argument('content_type', choices=['submission', 'comment'],
                        help='Type of content to retrieve (submission or comment)')
    parser.add_argument('--subreddit', default='all', help='Specify the subreddit you are interested on or "all" to read content from everywhere in Reddit')

    args = parser.parse_args()
    config = vars(args)

    getStreamedRedditContents(config["client_id"], config["secret_key"], config["content_type"], config["subreddit"])


if __name__ == "__main__":
    main()