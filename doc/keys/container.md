# "container"

CSS selector for element containing all your inner-elements you want to scrape

Example:

```html
<div class="outer">
	<div class="inner">
		<a href="link1.com">link1</a>
	</div>
	<div class="inner">
		<a href="link2.com">link2</a>
	</div>
	<div class="inner">
		<a href="link3.com">link3</a>
	</div>
</div>
```

A good CSS selector for this would be: `div[class=inner]`

Note:

`"container"` must be a CSS selector, not XPATH

The ability to make this XPATH compatible may be added in the future