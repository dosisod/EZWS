# self.check

If `self.check` is `True` then EZWS will check if each page is allowed in each sites `robots.txt` file

If `self.check` is `False` then EZWS will scrape any page regardless of the `robots.txt` file

It is reccommended that you keep `self.check` to `True` so you dont get banned/blocked for exceeding rate limits