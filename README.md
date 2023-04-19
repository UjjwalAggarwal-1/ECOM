# E-commerece backend

## prerequisites

- mysql
- python

## to run

1. when in this directory,at the same level as this file, create a virtual env using

```
python -m venv venv

```
or any preffered option

2. activate your venv

```
source venv/bin/activate

```

3. run 
```
pip install -r requirements.txt

```

4. in core/settings.py

        # set username of mysql server
        "USER": "username",
        # set password of mysql server
        "PASSWORD": "passwordforuser",
        "HOST": "localhost",
        # set port of mysql server
        "PORT": "3306",

### just above these lines we specified database name as 'e-commerce', which is same as the one used in sql file for creating database

5. run 
```
python manage.py runserver
```
when in this directory,at the same level as this file
