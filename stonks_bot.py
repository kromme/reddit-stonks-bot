import praw
import os
import re
import yaml


class StonksBot:
    """Scrape tickers from subreddits"""

    def __init__(self) -> None:

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
            self.tickers = f.readlines()

        with open("data/EU_tickers.txt", "r") as f:
            self.tickers += f.readlines()
