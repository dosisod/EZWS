# "grab"

The `"grab"` key stores an array of CSS/XPATH scrapable targets

Example:

```javascript
"grab":[
	{"xpath":"//div/text()"},
	{"css":"div", "contents":[""]}
]
```

Here, both the XPATH and the CSS selectors will be scraped