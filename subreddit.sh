# !/bin/sh

subreddits=("jackrussellterrier" "pugs" "corgis" "dachshunds")

for i in "${subreddits[@]}"
do 
	python3 'PATH/TO/subreddit_scraper.py' $i 10
	python3 'PATH/TO/email_files.py' $i
done