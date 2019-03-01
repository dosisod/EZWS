# Using XPATH to scrape

Inside of your `"grab"` key, you will have an array of dictionaries, each is a seperate scraping target

For XPATH you will have a single target which includes the data you want to scrape

Example:

For the HTML:

```html
<div class="card">
	<a href="link">Click here</a>
	<p class="desc">Description</p>
</div>
```

To scrape the first line (`a` tag), do this:

`{"xpath":"//div/a/text()"}`

To grab both the `a` tag and `p` tag innerTexts, do:

```
{"xpath":"//div/a/text()"},
{"xpath":"//div/p/text()"}
```

Make sure to put this inside of your `"grab"` key (as an array)

Instead of XPATH, you can also use [css selectors](css.md) or a mix of both if you want