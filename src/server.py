#!/usr/bin/env python
from app import app
from html_api import *
from json_api import api_v1


app.register_blueprint(api_v1)


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
