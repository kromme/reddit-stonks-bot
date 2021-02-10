# Reddit-stonks-bot
Scrape most mentioned stock tickers from subreddits like Wallstreetbets and Wallstreetbetsnew. Use it go to the moon!  
![wsb](https://upload.wikimedia.org/wikipedia/en/f/f0/WallStreetBets.png)  



## Usage
First get your credentials from [Reddit](https://praw.readthedocs.io/en/latest/getting_started/authentication.html). Either place them in a `creds.yaml`-file in the same folder as the `stonks_bot.py` or in environment variables. In either case use the following keys: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REDIRECT_URL, REDDIT_USER_AGENT.  

The output is printed and exported to output/mentions.csv in `append`-mode.
### Install requirements

```
git clone https://github.com/kromme/reddit-stonks-bot.git
cd reddit-stonks-bot
pip install -r requirements.txt
```


### Example YAML:
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
