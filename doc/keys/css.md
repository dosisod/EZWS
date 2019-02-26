# Using CSS Selectors to scrape

Inside of your `"grab"` key, you will have an array of dictionaries, each is a seperate scraping target

For CSS, you will have a target element and the attributes you want from the element once found

Example:

For the HTML:

```html
<div class="card">
	<a href="link">Click here</a>
	<p class="desc">Description</p>
</div>
```

To scrape the first line (`a` tag), do this:

`{"css":"a", "contents":[""]}`

Here, the target is all `a` tags within a `"container"`, and the attribute is the innertext

`"contents"` is an array of attributes you want to get from the `a` tag

Blank (`""`) strings will get the innertext ("Click here")

All other non-blank strings will pull an attribute of that name from the element

To grab the innertext and the href all at once, add `"href"` to the contents:

`{"css":"a", "contents":["","href"]}`

If there is only one item in `"contents"` then you dont have to have it in an array

The following examples are equivalent:

```javascript
{"css":"a", "contents":""}
{"css":"a", "contents":[""]}
```

Instead of CSS selectors, you can also use [xpath](xpath.md) or a mix of both if you want