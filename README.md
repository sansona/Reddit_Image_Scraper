# Reddit_Image_Scraper

Scraper that automatically scrapes new images from desired subreddits and emails to user(s). Scraper consists of three components.

1. subreddit_scraper.py - scrapes subreddit for new images and stores them in folder. Automatically compresses and archives old images.
2. email_files.py - emails list new images each time a new scrape is run. 

Both the above components can be used as standalones for scraping images and emailing images respectively. 

3. subreddit.sh - written to be run as a cron job (on Linux) or by Windows scheduler. Automates scraping and emailing such that one can scrape and email new posts from an array of subreddits for some repeated interval.

To use: 
  1. Setup new user credentials on reddit & Gmail such that there are unique user info for the bot - feed into user credentials   section in subreddit_scraper.py and email_files.py respectively
  2. Add in desired subreddits to scrape in subreddits.sh. I recommend r/wallpapers and r/astrophotography
  3. Set up cron job. I recommend scraping once a week such that the best posts bubble to the top of the subreddit when scraped - ``` 0 9 * * 0 bash 'PATH/TO/subreddit.sh' ```
