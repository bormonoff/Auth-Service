# Authorization service goal
In my free time, I like to dive (as deeply as my free time allows) into different areas of microservice architecture.

So, I decided to dive into the authorization/authentication topic, and that's how this repo was created.

## Basics
- Auth service is the service with the biggest load. I chose for the target more than 1M records in the database and 250K daily active users.
- For an auth model I chose to use JWT tokens and created a helper that handles all the JWT work to delve into that technology.
- For a password hasher I chose [argon2](https://en.wikipedia.org/wiki/Argon2).

## Important points:
- Each user has access and refresh tokens.
- Refresh tokens have a lifetime of $refresh_token_lifetime (14 days by default). Access tokens have a lifetime of $access_token_lifetime (2 hours by default).
- Refresh tokens are stored in the Postgres database.
- If a user refreshes his tokens, the server generates a new pair of tokens. It deletes the old refresh token from the Postgres database and puts the old access token in the Redis database.
- Each user has a role (subscriber, admin, superuser). This information is stored in the JWT token.
- The server provides CRUD operations for the roles.

For more information see the swagger docs or service function docs.

## Used technologies:
- Python
- Postgres
- Redis
- Fastapi
- Pytest
- Docker
- Poetry
- Pydantic
- Uvicorn

## How to launch (Linux/Mac)
**Docker compose should be installed.**

1. Clone the repository
 ```
- git clone git@github.com:bormonoff/auth_service.git
- cd $repo_folder
 ```
2. Copy .env file
 ```
- cp .env.example .env
 ```
2. Launch the docker-compose.yml
```
- sudo docker compose build
- sudo docker compose up
```
- As a result server generates OpenAPI docs and launches swagger.
- After that you can try Swagger via [link](http://localhost/auth/docs).

#### Optionaly launch tests (Linux/Mac)
- Tests need a running Postgres && Redis instance, which is why I created an additional docker-compose file.
1. Change the directory
 ```
- cd tests/func
 ```
2. Launch the docker-compose.yml
```
- sudo docker compose build
- sudo docker compose up
```
2. From another terminal launch pytest
```
- pytest .
```
#### Optionaly launch server in dev mode (Linux/Mac)
1. Download the dependencies
 ```
- poetry shell && poetry install
 ```
2. Launch containers with Postgres and Redis
3. Launch the server
```
- python3 src/main.py
```

---

*If you have any questions, please feel free to contact me on my personal telegram: `@bomron_off`*