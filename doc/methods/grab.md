# self.grab()

```python
grab(index=None)
```

When creating an EZWS object, you will specify a `file` param

This param can be an array, and you may want to specify which index you want to use

calling `grab()` with no index will grab every index that was set by the `file` param

Example:

```python
ez=EZWS(["file1.json", "file2.json"], useragent)

ez.grab(0) #grabs file1.json
ez.grab(1) #grabs file2.json
ez.grab() #grabs file1.json and file2.json
```

Note: everytime `grab()` is called, the output is appended to `self.output`

If you run an index twice, it will appear in the output twice