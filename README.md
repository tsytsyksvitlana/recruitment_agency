# WebApp for managing recruitment agency
[![Python](https://img.shields.io/badge/-Python-%233776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0a0a)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=0a0a0a)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/-Django%20Rest%20Framework-%2300B96F?style=for-the-badge&logo=django&logoColor=white&labelColor=0a0a0a)](https://www.django-rest-framework.org/)
[![SimpleJWT](https://img.shields.io/badge/-SimpleJWT-092E20?style=for-the-badge&logo=jsonwebtokens&logoColor=white&labelColor=0a0a0a)](https://github.com/jazzband/djangorestframework-simplejwt)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-%23316192?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=0a0a0a)](https://www.postgresql.org/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-yellow?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=0a0a0a)](https://pre-commit.com/)
[![isort](https://img.shields.io/badge/isort-enabled-brightgreen?style=for-the-badge&logo=isort&logoColor=white&labelColor=0a0a0a)](https://pycqa.github.io/isort/)
## Running aplication

1. Create and activate a virtual environment:

```
python -m venv myenv
```

On Windows:

```
myenv\Scripts\Activate
```

On Linux\MacOS:

```
source myenv/bin/activate
```
2. Install dependencies with:
```
poetry install
```
3. Run application
```
python manage.py runserver
```

## Migrations
1. To make migrations
```
python manage.py makemigrations
```
2. To run migrations
```
python manage.py migrate
```
## Pre-commit Command
```
pre-commit run --all-files
```
