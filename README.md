# instalyzer

Instagram Profile and Post Scraper and Sentiment Analyzer.

The original Selenium-based scraper relied on fragile CSS selectors
which no longer work with modern versions of Instagram. A new
`instaloader` based scraper is provided which interacts with
Instagram's official endpoints and is therefore more stable.

## Requirements

- Python 3.11+
- `instaloader` library (`pip install instaloader`)

## Usage

Run `instaloader_scraper.py` to download profile information and posts:

```bash
python instaloader_scraper.py
```

You will be prompted for a profile username and a JSON file containing
the collected data will be created in the current directory.
