# Running local

First, you have to clone this repository and have Docker installed on your machine.

After, inside the project folder you execute the following command in terminal:

```docker volume create --name=pgdata```

It creates a volume for our local database. Then, run:

```docker-compose up -d```
It will build the image of local django environment, and run the database also.

With your containers running now, you can go into the django container terminal:

```docker exec -it <django_container_id> /bin/bash```

Now you are controlling Django environment, you could generate migration, apply migrations, collect static and run server.

```export ENV_TYPE=local``` (to use local environment variables)

```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py collectstatic```

```python manage.py runserver 0.0.0.0:8000```

or even install new poetry dependencies:

```poetry install```

