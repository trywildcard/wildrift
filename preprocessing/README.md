# Install

`pip install -r requirements.txt`


# Setup

Add a file `twitterscraper/config.py`:

```python
twitter = {
    'key': '',
    'secret': '',
    'token': '',
    'token_secret': '',
}
```


# Run

```bash
python twitterscraper/scrape_twitter.py > graph.json
databench
```
