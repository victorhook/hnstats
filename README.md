# HackerNews web scraper

This is a simple tool to scrape statistics from [https://news.ycombinator.com/](HackerNews). The tool fetches *x* pages of posts and saves the statistics in a sqlite database, which later can be used for analysis.

### Usage

Ensure you have to python packages: `virtualenv env && source env/bin/activate && pip install -r requirements.txt`

Then you can edit the `fetch_hn.sh` script to include the correct path to *your* project. Then you can do:

`$ fetch_hn.sh --pages 5 --save`

or 

`$ fetch_hn.sh --help` for help.


To run the script every hour:
`$ crontab -e`
Add `*/60 * * * * PATH_TO_SCRIPT` to the file and you're done!
