# FastAPI Boilerplate with PostgreSQL, SQLAlchemy and API Key Authentication with Keys table

### Features
- Dockerized with Dockerfile and docker-compose to run the postgres database
- FastAPI
- PostgreSQL
- SQLAlchemy
- API Key Authentication


### Setup
- Set environment variables in .env_example file to DB USER PASS and change the name to .env
- Edit the docker-compose.yml file to set the database name and user
- Configure the docker files and
- openssl rand -base64 16 for a random DB password

### Run
```
docker compose --env-file ./app/.env up --build
```