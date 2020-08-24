Python version: 3.6

Django version: 3.1

prepare:

```
manage.py migrate
manage.py loaddata fixtures/test_data.json
manage.py test
manage.py runserver <ip>:<port>
```
