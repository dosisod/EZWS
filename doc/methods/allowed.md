# self.allowed()

```python
allowed(url)
```

Returns whether the specified site allows for parsing of the passed site based on the sites `robots.txt` file

If `self.check` is `False` the `allowed()` function will always return true

It is reccommended that you keep `self.check` to `True` so you dont get banned/blocked for exceeding rate limits