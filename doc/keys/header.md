# "header"

The `"header"` key allows for fixed width columns, while not including this key allows for variable width columns

For instance, a header like: `"header":["NAME","AGE"]` will only allow the first instance of each scraped value

```
If data is layed out like this on a page:

NAME
NAME
AGE

Where the name is what value it is associated with, a header like above will produce:

NAME,AGE

Whereas no header will produce:

NAME,NAME,AGE
```

Use the `header` key if you want to keep data structured, and where certain containers might have to of the same element

Dont use the `header` key if getting all the data from an element is needed, and order isnt wanted