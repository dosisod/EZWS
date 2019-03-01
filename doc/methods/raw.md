# self.raw

Contains the raw html of the most recently downloaded page (using `self.download()`)

`self.raw` may be useful after using `self.grab()` and still need to store the html directly

Note:

If multiple sites are scraped per grab, only the last scrape will be stored in `self.raw`

Note:

Changing the html doesnt effect the beautiful soup tree that was generated when `self.raw` was set

This does mean however that you will be unable to reload the tree with new data after changing raw