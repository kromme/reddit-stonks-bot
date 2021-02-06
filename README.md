# Reddit-stonks-bot
Scrape most mentioned stock tickers from Reddit

## Usage
First get your credentials from [Reddit](https://praw.readthedocs.io/en/latest/getting_started/authentication.html). Either place them in a `creds.yaml`-file in the same folder as the `stonks_bot.py` or in environment variables. In either case use the following keys: REDDIT_CLIENT_ID, 0REDDIT_CLIENT_SECRET, REDDIT_REDIRECT_URL, REDDIT_USER_AGENT.  

Example YAML:
```
REDDIT_CLIENT_ID: xxXXXxxXXxXXxX
REDDIT_CLIENT_SECRET: xxxx_xxxxxxxxxxxxxxxxxxxxxxxxxx
REDDIT_REDIRECT_URL: http://localhost:8080
REDDIT_USER_AGENT: testscript by u/xxxxxxx-xxxxxx
```

### From Command Line
```
python stonks_bot.py
```


### From Python
```
from stonks_bot import StonksBot
sb = StonksBot(number_of_posts=2000)
sb.find_tickers_on_reddit()
```
