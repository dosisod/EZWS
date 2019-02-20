# self.file

Stores config file path/obj

If `type(self.file)` is a string, it will be assumed that file the path to a filename

If `type(self.file)` is a dictionary, it is assumed that file is a json object and loaded directly

Examples:

```
#passes filename
ez=EZWS("input.json", useragent)

#passes config json directly
json={
	"links":[
		# ...
	]
}
ez=EZWS(json, useragent)
```

Default is `"config.json"`