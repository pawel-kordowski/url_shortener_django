# url shortener
A small project to create and retrieve short form of long urls.

### how to run app locally
```shell
cp .env.example .env
make up
```

### how to run tests locally
```shell
cp .env.example .env
make test
```

### example HTTP requests
* create url via POST to `/urls/`
```shell
$ curl --request POST 'http://localhost:8000/urls/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://google.com"
}'

{"orig_url":"http://google.com","short_url":"http://localhost:8000/dzltR/"}
```
* retrieve url (get redirect) via GET to `/{url}/`
```shell
$ curl http://localhost:8000/dzltR/ -v
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8000 (#0)
> GET /dzltR/ HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.58.0
> Accept: */*
> 
< HTTP/1.1 302 Found
< Date: Wed, 08 Jun 2022 18:53:56 GMT
< Server: WSGIServer/0.2 CPython/3.10.5
< Content-Type: text/html; charset=utf-8
< Location: http://google.com
< X-Frame-Options: DENY
< Content-Length: 0
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
* Connection #0 to host localhost left intact
```

### tech stack
* PostgreSQL as a database
* Django as a web framework, ORM, migrations tool and local web server
* django-rest-framework to implement one of the endpoints
* redis as a cache layer
* pytest for unit tests
* factory-boy for generating database objects in tests
* poetry to manage python packages
* docker and docker-compose to create local environment
* black, flake8 and isort to keep code quality


### architecture
All the business logic is kept in query set and model class.
