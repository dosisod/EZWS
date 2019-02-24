# "url"

`"url"` stores a single url or an array of urls to parse

This key does inside of [links](links.md) key, eg:

```kavascript
"links":[
	{
		"url":["",""]
	}
]
```

urls inside of `"url"` must have a protocol such as http or https

Examples:

```javascript
"url": ["http://google.com", "https://ddg.gg"] //both valid

"url": ["localhost:1234", "example.com"] //both invalid
```