# DoS Rate Limit Middleware

This is a middleware designed for DoS rate limiting in Django. 

## Follow the below steps to configure this in Django application

In your Django project, create a new middleware file.

- Create a file rate_limit_middleware.py in one of your app directories inside middleware folder in your Django project.

- Add the following rate-limiting code adapted for Django:
 [Rate_Limit_Middleware](https://github.com/akashgalagali/DoS-Rate-Limit-)

-  Register the Middleware in settings.py

```python

MIDDLEWARE = [
    ...
    'your_app.middleware.rate_limit_middleware.RateLimitMiddleware',
    ...
]

```
- location of middleware folder in Django project.
``` 
 your_project/
 │
 ├── your_app/
 │   ├── __init__.py
 │   ├── models.py
 │   ├── views.py
 │   ├── middleware/          # Middleware folder
 │   │   └── rate_limit_middleware.py  # Your middleware file
 │   └── other_files.py
 │
 ├── your_project/
 │   ├── __init__.py
 │   ├── settings.py          # Django settings file
 │   ├── urls.py
 │   └── wsgi.py
 │
 └── manage.py
```
- configure below three constants according to requirement:
> - RATE_LIMIT = 3  # Set the maximum number of allowed requests 
> - TIME_WINDOW = 1  # Define the time window (in seconds) for enforcing the rate limit
> - BLOCK_DURATION = 20  # Specify the duration (in seconds) for which an IP will be blocked

## Position of middleware in the request/response cycle

```
    Client (Browser)
           |
           v
    -----------------
    |   HTTP Request   |
    -----------------
           |
           v
    +------------------+
    |   URL Routing    |
    +------------------+
           |
           v
    +------------------+
    |   Middleware 1   |  <-- Processing order for requests
    +------------------+
           |
           v
    +------------------+
    |   Middleware 2   |
    +------------------+
           |
           v
    +------------------+
    |   View Function   |
    +------------------+
           |
           v
    +------------------+
    |   Middleware 2   |  <-- Processing order for responses (reversed)
    +------------------+
           |
           v
    +------------------+
    |   Middleware 1   |
    +------------------+
           |
           v
    -----------------
    |  HTTP Response   |
    -----------------
           |
           v
    Client (Browser)
```