# self.output

Stores a file path to output `.csv` file

Setting `self.output=False` will disable file outputing all together

output file is an init param for the EZWS class, so you can create an object with a different path using:

```
ez=EZWS("config.json", useragent, output="path/output.csv")
# or
ez=EZWS("config.json", useragent, output=False)
```

By default `self.data` is set to `"output.csv"`