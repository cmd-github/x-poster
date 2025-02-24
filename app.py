import feedparser
import tweepy
import time
import random
import os
import sys

# List of RSS feeds
RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cryptoslate.com/feed/"
]

# List of comments to add variety
# List of comments to add variety
COMMENTS = [
    "Don't miss this!",
    "Hot off the press!",
    "Crypto moves!",
    "See for yourself!",
    "This one's trending!",
    "Eye-opening update!",
    "What do you think?",
    "Another milestone!",
    "Worth your time!",
    "This could be huge!",
    "Keeping you updated!",
    "Heads up!",
    "New developments!",
    "Must-read!",
    "Key update here!",
    "Fresh insight!"
]

# Static website to include
WEBSITE = "www.cmdtech.co.uk"  # Replace with your desired URL

# Default API key file
DEFAULT_KEY_FILE = "client1.txt"

def load_api_keys(key_file):
    prefix = key_file.replace('.txt', '').upper()
    return {
        "consumer_key": os.environ[f"{prefix}_CONSUMER_KEY"],
        "consumer_secret": os.environ[f"{prefix}_CONSUMER_SECRET"],
        "access_token": os.environ[f"{prefix}_ACCESS_TOKEN"],
        "access_token_secret": os.environ[f"{prefix}_ACCESS_TOKEN_SECRET"]
    }

def post_tweet(key_file):
    """Post a random RSS feed item to X with a website and comment."""
    # Load API keys
    keys = load_api_keys(key_file)

    # Set up Tweepy Client for v2 API
    client = tweepy.Client(
        consumer_key=keys["consumer_key"],
        consumer_secret=keys["consumer_secret"],
        access_token=keys["access_token"],
        access_token_secret=keys["access_token_secret"]
    )

    # Pick a random RSS feed and comment
    rss_url = random.choice(RSS_FEEDS)
    comment = random.choice(COMMENTS)
    feed = feedparser.parse(rss_url)

    # Construct the tweet
    for entry in feed.entries[:1]:
        base_post = f"{entry.title} {WEBSITE} {comment}"
        # Trim to fit 280 characters if needed
        if len(base_post) > 280:
            # Calculate how much title we can keep
            max_title_len = 280 - len(f" {WEBSITE} {comment}")
            trimmed_title = entry.title[:max_title_len-3] + "..."
            post = f"{comment} {trimmed_title} {WEBSITE} "
        else:
            post = base_post

        try:
            response = client.create_tweet(text=post)
            print(f"[{time.ctime()}] Posted to {key_file}: {post}, Tweet ID: {response.data['id']}")
        except tweepy.TweepyException as e:
            print(f"[{time.ctime()}] Error with {key_file}: {e}")

if __name__ == "__main__":
    # Use command-line argument for key file, or default
    key_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_KEY_FILE
    post_tweet(key_file)