# FastAPI

[FastAPI](https://fastapi.tiangolo.com) is:
> a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based 
> on standard Python type hints.

It is important to understand that FastAPI is an ASGI Application Framework. It cannot serve anything
by itself: it needs an ASGI Server (or a WSGI server with an ASGI worker).

## About WSGI and ASGI

[WSGI](https://www.fullstackpython.com/wsgi-servers.html) stands for *Web Server Gateway Interface*,
and ASGI for *Asynchronous Server Gateway interface*.
They both specify an interface that sits in between a web server and a Python web application or framework.
WSGI has been around for a long time. ASGI is a spiritual successor to WSGI, that is able to handle
asynchronous requests and responses.

In short, an **(A|W)SGI Server** is a web server that is able to call python code when it receives an HTTP request.
The way it calls this code, and what parameters are passed to the calling function, are all specified in the
(A|W)SGI interface specification. It includes information about the request and the environment.

It is then the role of the **(A|W)SGI Application** to build the headers and to return the data as iterable.
This is done using the `start_response` call. Here is a simple WSGI application
([source](http://ivory.idyll.org/articles/wsgi-intro/what-is-wsgi.html)):

```python
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    # Actually start sending data back to the server
    start_response('200 OK', response_headers)
    return ['Hello world!\n']
```

This `simple_app` can then be passed to a server and be served as is.

Of course, apps are usually way more complex, with routing, proxies and complex logic involved.
This is why we use **(A|W)SGI Application Frameworks** such as FastAPI. Those frameworks have a single
entrypoint (that is called by the server), and lots of conveniencies to abstract the complexities of
constructing responses, handling errors, doing redirects, determining which code to execute, etc.

![WSGI overview](assets/01-wsgi.excalidraw.png)

To actually run a FastAPI app, we thus need an ASGI server (or a WSGI server with an ASGI-compatible worker).
In development, we can use [uvicorn](https://uvicorn.org/) - a minimalist server with a single process.

While a single process is enough for testing, it is not suitable for production.
The most common production setup for FastAPI is [gunicorn](https://gunicorn.org/)
with [uvicorn workers](https://fastapi.tiangolo.com/deployment/server-workers/), sitting behind
a reverse proxy such as [Nginx](https://www.nginx.com/).

Why the reverse proxy you ask? 
Gunicorn is amazing at handling workers and WSGI-specific things, while NGINX is a full-featured
HTTP server, able to handle millions of concurrent connections, provide DoD protection,
rewrite headers, and serve static resources more effectively.
Together, they form the perfect team.


See also: [The Layered World Of Web Development: Why I Need NGINX And UWSGI To Run A Python App?](
http://www.ines-panker.com/2020/02/16/nginx-uwsqi.html)

## Install FastAPI + uvicorn

Anyway, to get started, we only need to install both FastAPI and uvicorn:
```bash
poetry add fastapi 'uvicorn[standard]'
```

The uvicorn server can then be launched (with reload!) using:
```bash
uvicorn package.filename:app_object --reload
```

## Create an app

Create a file `fastapi_celery/main.py` and add:

```python
from fastapi import FastAPI
from typing import Dict 

app = FastAPI() # <- the ASGI entrypoint

@app.get('/')
def index() -> Dict:
    return {'greating': 'hello'}
```

Run uvicorn with reload:
```bash
uvicorn fastapi_celery.main:app --reload
```

and try it using:
```bash
curl http://localhost:8000/
```

Congrats! You have successfully coded a REST API.

Now, open the following in your browser: `http://localhost:8000/docs`.
FastAPI comes built-in with a [Swagger UI](https://swagger.io/tools/swagger-ui/
the [OpenApi](https://spec.openapis.org/oas/latest.html) specification for us, based on type hints.

The documentation is already good, but we can make it better.

## Improve the docs

First, add a description:
```python
@app.get('/', description="returns hello world")
```

The return type being a dictionary, FastAPI cannot give much detail.
Let's improve that. First, install pydantic:
```bash
poetry add pydantic
```

And add a class for your return type:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Hello(BaseModel):
    greating: str
    date: datetime

@app.get('/', description="returns hello world")
def index() -> Hello:
    return Hello(greating="hello", date=datetime.now())
```

Have a look at the successful response example in the docs. Isn't it great?

## Exceptions

To return exceptions to the user, use the `HTTPException` class:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get('/error')
def error():
    raise HTTPException(status_code=500, detail="Just throwing an internal server error")
```

Just try it:
```bash
curl http://localhost:8000/error -v
# < HTTP/1.1 500 Internal Server Error
# {"detail":"Just throwing an internal server error"}
```

## Inputs

### Query and path parameters

Now, try to add a default parameter to one of the methods, and see how it looks in the docs.
For example:

```python
@app.get('/', description="says hello")
def index(name: str) -> str:
    return f"hello {name}!"
```

Try also to set a default value for `name`. How does it look now in the docs?

To transform this query parameter into a path parameter, use the `{}` in the path.
You should recognize this if you used Django or Flask:

```python
@app.get('/hello/{name}', description="says hello using path parameter")
def index(name: str) -> str:
    return f"hello {name}!"
```

The type hint on the parameter is sufficient for FastAPI to do basic validation (e.g. `int`).

### Request body

We can also do POSTs as easily:
```python
@app.post('/post')
def post(hello: Hello) -> str:
    return hello.greating

@app.post('/postd')
def post_dict(hello: Dict) -> Dict:
    return hello
```

The body must be a `Dict`, or a subclass of `pydantic.BaseModel`. Other simple arguments
are still supported (query or path parameters).

Don't forget to run the following to format correctly your code:
```bash
poetry run black fastapi_celery
```

## Input validation

FastAPI already supports built-in validation for types such as `Email`, `UUID`, `URL`, etc.
Sometimes though we need additional validation on the input.

This can be achieved using `Query`, `Path` and `Body`.

### On query parameters

Validation is only available for query parameters **of type `str`** :face_with_raised_eyebrow:.
Here is an example:

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/greating")
def greating(name: str = Query(min_length=2, regex="[a-z]+")) -> str:
    return f"hello {name}"
```

A working request would be`curl http://localhost:8000/greating\?name\=xyz`. And what happens on bad input?

```bash
curl http://localhost:8000/greating\?name\=x | json_pp
# {
#    "detail" : [
#       {
#          "ctx" : {
#             "limit_value" : 2
#          },
#          "loc" : [
#             "query",
#             "name"
#          ],
#          "msg" : "ensure this value has at least 2 characters",
#          "type" : "value_error.any_str.min_length"
#       }
#    ]
# }                  
```

### On path parameters

Path parameters can be validated similarly, this time using `Path`.
Note that `Path` relies on pydantic's `Field` under the hood, and thus supports
many more validation and types (see body parameters for more examples).

Here is a simple example:
```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/greating/{name}/{age}")
def greating(
    name: str = Path(min_length=2, regex="[a-z]+"), age: int = Path(ge=9, le=120)
) -> str:
    return f"hello {name}, you age is {age}"
```

### On body parameters

Given the body is defined as a class extending pydantic's `BaseModel`,
one can use pydantic's `Field` in the model declaration. But this is not enough!
We also need to instantiate a `Body` in FastAPI's method definition.

An example is worth a thousand words:

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

class Person(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=9, le=120)


# We need to initialize person with Body(), or the validation
# won't occur
@app.post("/")
def post(person: Person = Body()) -> str:
    return f"hello {person.name}, your age is {person.age}"
```

## Going further

FastAPI's documentation is amazing (way better than this one)!

:arrow_right: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)