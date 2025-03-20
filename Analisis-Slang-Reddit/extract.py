import praw
from dotenv import load_dotenv
import os
import pandas as pd
import time
from prawcore.exceptions import TooManyRequests

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Set up Reddit API client
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# List of subreddits to fetch data from
subreddits = ['AskReddit', 'funny', 'memes', 'teenagers', 'OutOfTheLoop', 'soccer', 'gaming', 'NoStupidQuestions']
total_posts_needed = 5000  # Total number of posts to fetch
posts_per_subreddit = total_posts_needed // len(subreddits)  # Fetch evenly from each subreddit

# Create a list to hold the fetched data
data = []

# Fetch posts from each subreddit
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    count = 0
    for submission in subreddit.hot(limit=posts_per_subreddit):
        try:
            title = submission.title
            text = submission.selftext
            upvotes = submission.score
            comments_count = submission.num_comments
            timestamp = submission.created_utc
            subreddit_name = submission.subreddit.display_name

            # Extracting comments
            comments_data = []
            submission.comments.replace_more(limit=0)  # This removes 'MoreComments' objects that can be tricky to handle
            for comment in submission.comments.list():
                comment_text = comment.body
                comment_upvotes = comment.score
                comment_timestamp = comment.created_utc
                comments_data.append([comment_text, comment_upvotes, comment_timestamp])

            # Add post data
            data.append([title, text, upvotes, comments_count, timestamp, subreddit_name, comments_data])

            count += 1
            if count >= posts_per_subreddit:
                break

        except TooManyRequests as e:
            print("Rate limit hit. Sleeping for 60 seconds...")
            time.sleep(60)  # Sleep for 60 seconds before retrying
            continue

        # Optional: Sleep for a few seconds between requests to reduce the risk of hitting rate limits
        time.sleep(2)  # Adjust the sleep time if needed

# Convert to a pandas DataFrame
df = pd.DataFrame(data, columns=['Title', 'Text', 'Upvotes', 'Comments', 'Timestamp', 'Subreddit', 'Comments Data'])

# Save the raw data to a CSV (optional)
df.to_csv('reddit_data_with_comments.csv', index=False)

# Display the first few rows
print(df.head())
