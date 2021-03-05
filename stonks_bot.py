import os
import re
from collections import Counter
from datetime import datetime, timedelta

import pandas as pd
import praw
import yaml
from praw.models import MoreComments
from tqdm import tqdm

from constants import BLACKLIST_WORDS


class StonksBot:
    """Scrape tickers from subreddits
    :param subreddit: names of subreddits to scraper
    :param number_of_posts: maximum number of posts per subreddit
    :param number_of_days: number of days to look back

    Usage:
    from stonks_bot import StonksBot
    sb = StonksBot(number_of_posts=10)
    sb.find_tickers_on_reddit()
    """

    def __init__(
        self,
        subreddit=["wallstreetbets", "wallstreetbetsnew"],
        number_of_posts: int = 2000,
        number_of_days: int = 1,
    ) -> None:

        self.subreddits = subreddit if isinstance(subreddit, list) else [subreddit]
        self.number_of_posts = number_of_posts
        self.number_of_days = number_of_days

        # init Reddit account
        self._init_reddit_account()

        # load tickers
        self._load_tickers()

    def _init_reddit_account(self) -> None:
        """Signing in to Reddit"""
        # init variables
        REDDIT_CLIENT_ID = False
        REDDIT_CLIENT_SECRET = False
        REDDIT_REDIRECT_URL = False
        REDDIT_USER_AGENT = False

        # either load from OS vars
        if "REDDIT_CLIENT_ID" in os.environ.keys():
            REDDIT_CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
            REDDIT_CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
            REDDIT_REDIRECT_URL = os.environ["REDDIT_REDIRECT_URL"]
            REDDIT_USER_AGENT = os.environ["REDDIT_USER_AGENT"]

        # or from YAML
        else:
            with open("creds.yaml") as f:
                creds = yaml.load(f, Loader=yaml.FullLoader)
            REDDIT_CLIENT_ID = creds["REDDIT_CLIENT_ID"]
            REDDIT_CLIENT_SECRET = creds["REDDIT_CLIENT_SECRET"]
            REDDIT_REDIRECT_URL = creds["REDDIT_REDIRECT_URL"]
            REDDIT_USER_AGENT = creds["REDDIT_USER_AGENT"]

        assert (
            REDDIT_CLIENT_ID
        ), "Credentials not found. Go to https://praw.readthedocs.io/en/latest/getting_started/authentication.html and get your credentials. Either place them in a `creds.yaml`-file or in environment variables. In either case use the following keys: REDDIT_CLIENT_ID, 0REDDIT_CLIENT_SECRET, REDDIT_REDIRECT_URL, REDDIT_USER_AGENT"

        # sign in
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            redirect_uri=REDDIT_REDIRECT_URL,
            user_agent=REDDIT_USER_AGENT,
        )

        self.reddit.read_only = True

    def _load_tickers(self) -> None:
        """Load ticker information
        Downloaded from https://github.com/shilewenuw/get_all_tickers/tree/master/get_all_tickers
        """

        with open("data/tickers.txt", "r") as f:
            tickers = f.readlines()

        with open("data/EU_tickers.txt", "r") as f:
            tickers += f.readlines()

        tickers = [str(t).replace("\n", "").strip() for t in tickers]
        tickers = [t for t in tickers if len(t) > 1]

        self.RE_TICKERS = re.compile(r"\b(" + "|".join(tickers) + r")\b")

    def find_tickers(self, text: str) -> list:
        """find all tickers in a text"""
        return [
            ticker
            for ticker in self.RE_TICKERS.findall(text)
            if ticker not in BLACKLIST_WORDS
        ]

    def find_tickers_in_post(self, post) -> list:
        """Find al tickers in a title and comments
        :param post: A Reddit Post
        """
        found_tickers = []
        # skip if already seen
        if post.clicked:
            return []

        # check whether post is not too old
        ts_post = datetime.fromtimestamp(post.created_utc)
        ts_range = datetime.now() - timedelta(days=self.number_of_days)
        if ts_post < ts_range:
            return []

        # check title
        found_tickers += self.find_tickers(post.title)

        for comment in post.comments:
            if isinstance(comment, MoreComments):
                continue

            # check tickers
            found_tickers += self.find_tickers(comment.body)

            # comment has replies
            replies = comment.replies
            for reply in replies:
                if isinstance(reply, MoreComments):
                    continue

                # check tickers in reply
                found_tickers += self.find_tickers(reply.body)

        return found_tickers

    def find_tickers_in_subreddit(self, subreddit: str) -> list:
        """Loop through posts of a subreddit
        :param subreddit: name of the subreddit
        """
        print(f"\nReading {subreddit}")
        sub = self.reddit.subreddit(subreddit)
        posts = sub.new(limit=self.number_of_posts)

        found_tickers = []
        for _, post in tqdm(enumerate(posts)):
            found_tickers += self.find_tickers_in_post(post)

        return found_tickers

    def find_tickers_on_reddit(self):
        """loop through all subreddits"""

        found_tickers = []
        for _, subreddit in enumerate(self.subreddits):
            found_tickers += self.find_tickers_in_subreddit(subreddit)

        # count and to df
        count = Counter(found_tickers)
        df = (
            pd.Series(count)
            .to_frame("mentions")
            .reset_index()
            .rename(columns={"index": "ticker"})
        )

        print("\n\n Found the following tickers:")
        print(df.sort_values(by="mentions", ascending=False).head(10))

        # add timestamp
        df["ts"] = datetime.now()

        # output
        if not os.path.exists("output"):
            os.mkdir("output")
        df[["ts", "ticker", "mentions"]].to_csv(
            "output/mentions.csv", index=False, mode="a", header=False
        )


if __name__ == "__main__":
    # init Stonks Bot
    sb = StonksBot(number_of_posts=2000)

    # Run ano to the moon!
    sb.find_tickers_on_reddit()