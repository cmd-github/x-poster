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

# Static website to include
WEBSITE = "www.coindesk.com"

# Default API key file
DEFAULT_KEY_FILE = "client1.txt"

def load_api_keys(key_file):
    """Load API keys from environment variables or a local file."""
    prefix = key_file.replace('.txt', '').upper()
    env_keys = {
        "consumer_key": f"{prefix}_CONSUMER_KEY",
        "consumer_secret": f"{prefix}_CONSUMER_SECRET",
        "access_token": f"{prefix}_ACCESS_TOKEN",
        "access_token_secret": f"{prefix}_ACCESS_TOKEN_SECRET"
    }
    
    # Try environment variables first (GitHub Actions)
    if all(key in os.environ for key in env_keys.values()):
        return {
            "consumer_key": os.environ[env_keys["consumer_key"]],
            "consumer_secret": os.environ[env_keys["consumer_secret"]],
            "access_token": os.environ[env_keys["access_token"]],
            "access_token_secret": os.environ[env_keys["access_token_secret"]]
        }
    # Fallback to local file (local testing)
    else:
        try:
            with open(key_file, "r") as f:
                lines = f.read().splitlines()
                if len(lines) != 4:
                    raise ValueError("Key file must contain 4 lines: Consumer Key, Consumer Secret, Access Token, Access Token Secret")
                return {
                    "consumer_key": lines[0].strip(),
                    "consumer_secret": lines[1].strip(),
                    "access_token": lines[2].strip(),
                    "access_token_secret": lines[3].strip()
                }
        except FileNotFoundError:
            print(f"Error: {key_file} not found in {os.getcwd()}. Please create it or set environment variables.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading {key_file}: {e}")
            sys.exit(1)

def post_tweet(key_file):
    """Post a random RSS feed item to X with a hyperlinked website."""
    # Load API keys
    keys = load_api_keys(key_file)

    # Set up Tweepy Client for v2 API
    client = tweepy.Client(
        consumer_key=keys["consumer_key"],
        consumer_secret=keys["consumer_secret"],
        access_token=keys["access_token"],
        access_token_secret=keys["access_token_secret"]
    )

    # Pick a random RSS feed
    rss_url = random.choice(RSS_FEEDS)
    feed = feedparser.parse(rss_url)

    # Construct the tweet
    for entry in feed.entries[:1]:
        # Format the tweet with the website, blank line, title, and link
        base_post = f"{WEBSITE}\n\n{entry.title}\n{entry.link}"

        # Trim to fit 280 characters if needed
        if len(base_post) > 280:
            max_title_len = 280 - len(WEBSITE) - len(entry.link) - 5  # 5 for newline and "..."
            trimmed_title = entry.title[:max_title_len] + "..."
            post = f"{WEBSITE}\n\n{trimmed_title}\n{entry.link}"
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