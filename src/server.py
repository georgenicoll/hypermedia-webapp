#!/usr/bin/env python
from app import app
from html_api import *
from json_api import api_v1
from hxml_api import hxml_api


app.register_blueprint(api_v1)
app.register_blueprint(hxml_api)


def main() -> None:
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
