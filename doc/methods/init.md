# self.__init__()

```python
__init__(file, ua, check=True, output="output.csv")
```

# `file`

File object, either a filename string, JSON object of config, or array containing a combination

Read more about the file object [here](file.md)

# `ua`

Short for "user-agent", this is what your scraper will identify itself as when scraping a server

Make sure your user-agent is unique to your bot and not associated with an existing bot

# `check`

`True`: Checks whether your bot is allowed to scrape a certain site/url of site

`False`: Scrapes site whether you are allowed to or not

Read more [here](check.md)

# `output`

Specifies where to direct output to

String type will save it as filename passed

Setting it to `False` will disable file outputting

Read more [here](output.md)