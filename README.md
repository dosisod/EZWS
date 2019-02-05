# EZWS
Easy Web Scrape: Use CSS selectors to scrape websites in python

# Usage

By looking at the HTML structure of a webpage, you can use CSS selectors to grab the data you want

Use as many different links as you want, each one having a container tag, and CSS selectors that grab desired data from each container

HTML example:

```html
<!-- index.html -->
<div class="contact">
	<p class="name">Raymond King</p>
	<p class="spacer">-----</p>
	<a class="website" href="raymondking.com">raymondking.com</a>
</div>
<div class="contact">
	<p class="name">Lawrence Harris</p>
	<p class="spacer">-----</p>
	<a class="website" href="lawrence.com">lawrence.com</a>
</div>
<div class="contact">
	<p class="name">Christine Martinez</p>
	<p class="spacer">-----</p>
	<a class="website" href="christinephotos.io">christinephotos.io</a>
</div>
```

The HTML above could be scraped with json file that looks something like this:

```javascript
{
    "header":["NAME","LINK","INNER"],
	"links":[ //allows for many links, using formatting below
		{
			"url":"http://0.0.0.0:1234/index.html",
			"container":"div[class=contact]", //identifier for element holding desired content
			"grab":[
				{"css":"p[class=name]", "contents":[""]}, //grab just the innertext ("")
				{"css":"a", "contents":["href",""]} //grab href and innertext
			]
		} //more links could be added after this
	]
}
```

Resulting in a CSV file like this:

```
NAME,LINK,INNER
Raymond King,raymondking.com,raymondking.com
Lawrence Harris,lawrence.com,lawrence.com
Christine Martinez,christinephotos.io,christinephotos.io
```