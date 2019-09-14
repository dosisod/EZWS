# "url"

`"url"` stores a single url or an array of urls to parse

This key goes inside of the [links](links.md) key, eg:

```javascript
"links":[
	{
		"url": ""
	}
]
```

urls inside of `"url"` must have a protocol such as http or https

Examples:

```javascript
"url": ["http://google.com", "https://ddg.gg"] //both valid

"url": ["localhost:1234", "example.com"] //both invalid
```

## Enumeration

`"url"` strings can contain special syntax (`{{}}}`) for parsing similar or repeating link

`{{}}` Syntaxing is as follows:

| Syntax | Example | Description |
| ------ | ------- | ----------- |
| `{{START-END}}` | `page{{0-1000}}.html` | Counts by one from `START` to `END` (where `END` is inclusive) |
| `{{START-END,STEP}}` | `page{{0-1000,2}}.html` | Counts by `STEP` from `START` to `END` (where `END` is inclusive) |
| `{{A|B|C}}` | `website.{{org|com|edu}}` | Enumerates all seperated by a `|` |

`{{}}`s can be combined in a single url to create more complex templates:

`"http://{{docs|sheets|slides}}.google.com/test/{{0-2}}/"` will create parse the following urls:

```
http://docs.google.com/test/0/
http://docs.google.com/test/1/
http://docs.google.com/test/2/
http://sheets.google.com/test/0/
http://sheets.google.com/test/1/
http://sheets.google.com/test/2/
http://slides.google.com/test/0/
http://slides.google.com/test/1/
http://slides.google.com/test/2/
```