# Web server with request rate limitation

This is a simple web server which counts the number of requests per session and blocks the request if the request was overly maiden.

By default the webserver accepts 100 requests per 1 hour, per a session. Every request over the limitation will be rejected while the server has 100 requests within last single hour from the session.

# Prerequisites

The web server is using Python3, and was built on [Flask](https://flask.palletsprojects.com/en/1.1.x/) and using [pytest](https://docs.pytest.org/en/6.2.x/) for testing. Following shell commands would resolve the dependency issue.

```
$ pip install flask
$ pip install pytest
```

# How to run

```
$ export FLASK_APP=main.py
$ flask run
```
