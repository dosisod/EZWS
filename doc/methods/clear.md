# self.clear()

```python
clear()
```

Clears the internal state of `self.data`

Example:

```python
ez=EZWS("file.json", useragent)
ez.grab() # [ stuff ]
ez.grab() # [ stuff, stuff ]
ez.clear() # []
ez.grab() # [stuff ]

#stuff refers to data from grab()
```