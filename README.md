<div align="center">
    <h1>Travel Recommendation</h1>
</div>


<div align="center">
    <img src="https://img.shields.io/badge/Python-3.10-green" />
    <img src="https://img.shields.io/badge/Django-%3E%3D5.0.4%2C%3C5.1.0-blue">
    <img src="https://img.shields.io/badge/djangorestframework-%3E%3D3.15.1%2C%3C3.16.0-red">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json"/>
</div>



---


## Indexes
- [Prerequisites](#prerequisites)
- [Database Setup in Docker](#database-setup-in-docker-optional---local)
- [Project Setup](#project-setup)
- [Create Virtualenv](#create-and-activate-virtual-environment)
- [Install New Libraries](#install-libraries)
- [Format & Lint Code](#apply-code-format--linting)
- [Run project](#run-the-project)
- [Create Superuser](#create-superuser)



---


### Prerequisites
- Python >= 3.10
- uv => `pip install uv`
- PostgreSQL


### Database setup in Docker (Optional - Local)
```shell
1. docker run -p 5432:5432 --name db -e POSTGRES_PASSWORD=postgres -d postgres
2. docker exec -it db bash
3. su - postgres
4. psql
5. create database <database_name>;
6. create user <database_user> with encrypted password 'password';
7. grant all privileges on database <database_name> to <database_user>;
9. exit 
```


### Project Setup:
```shell
 cp .secrets.example.yaml .secrets.yaml
```
:warning: Please do not edit `requirements.txt` manually.


##### Create and Activate virtual environment
```shell
1. uv venv
2. source .venv/bin/activate
```


##### To add new libraries first update `pyproject.toml`.
```shell
uv pip compile -o requirements.txt pyproject.toml
```


##### Install libraries 
```shell
uv pip sync requirements.txt
```
##### Apply Code Format & Linting
```shell
1. ruff format . # format
2. ruff check . # lint
```
### Run the project (locally)
```shell
python manage.py runserver
```

##### Create superuser
```shell
python manage.py createsuperuser
```

