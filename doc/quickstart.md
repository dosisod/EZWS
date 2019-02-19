# Quickstart

This quickstart guide will give you the basics needed to start doing basic scraping using EZWS

For this demo, all examples are stored in a json file called `config.json`

# Single URL, single grab

To grab one thing from one url, one could do:

```javascript
{
	"links":[
		{
			"url":"http://example.com",
			"container":"div",
			"grab":[{"css":"a", "contents":[""]}]
		}
	]
}
```

In this example:

* Only the website `example.com` will be scraped

* EZWS will grab all the `div` elements

* EZWS will go through and get all `a` tags in the `div`

* Using `""` will return the innertext of every `a` tag in every `div`

# Many attributes from one element

If you want to grab both an `href` and a innertext for every `a` tag, try:

```javascript
"grab":[{"css":"a", "contents":["","href"]}]
```

This will grab the innertext, then the href for each `a` tag

# Grab many elements from a container

EZWS will find all containers matching the `"container"` key

Inside each container, you may want many different elements

The `"grab"` key takes an array, so by adding another element:

```javascript
"grab":[
	{"css":"a", "contents":["href"]},
	{"css":"p", "contents":[""]}
]
```

This example will:

* Find all `a` tags inside container, and grab its `href` attribute

* Then, find all `p` tags inside the container, and return its innertext

# Running it

Once you have your `config.json` file, you are ready to start scraping

To run, you must specify a user-agent that is unique to your bot

This allows web servers to differentiate between bots and ban them if need be

```python
ua="change this value"
ez=EZWS("config.json", ua)
ez.grab()
```

Done! By default an `output.csv` file will be created storing scraped values