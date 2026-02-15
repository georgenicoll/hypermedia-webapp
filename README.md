# hypermedia-webapp
Working through https://hypermedia.systems/a-web-1-0-application/

## Installing/Updating js dependencies

```shell
HTMX_VERSION=2.0.8 # This should match the value in layout.html
curl https://cdn.jsdelivr.net/npm/htmx.org@${HTMX_VERSION}/dist/htmx.js -o src/static/js/htmx.${HTMX_VERSION}.js
```

## Run

Run using uv:

```shell
uv run hypermedia-webapp
```

or, to have changes trigger a reload:

```shell
uv run dev-server
```

## Original full version

See [https://github.com/bigskysoftware/contact-app](https://github.com/bigskysoftware/contact-app)
