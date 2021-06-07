# Weather API

## Introduction 
To send Excel weather report to list of email ids

### To run the application

make sure that rabbitmq and python are installed on your system and correctly configured to run this application.
1. clone the repo -> git clone git@github.com:arjunsunil/weather-api.git
2. install the packages from requirements.txt -> pip install -r requirements.txt
3. run the server -> python manage.py runserver

### Create a superuser

run "python manage.py createsuperuser"` 

log in to `http://127.0.0.1:8000/admin/` 

## API List

1. Login `http://127.0.0.1:8000/api/auth/login`(POST)
 
Input body
{
    "username": "arjun",
    "password": "arjun@123#"
}

2. Weather list `http://127.0.0.1:8000/api/weather/list?limit=1&offset=0`(GET)

3. Send Email `http://127.0.0.1:8000/api/send/email/`

Input body
{
    "emails": ['arjunpp.sunil@gmail.com']
}

4. Login `http://127.0.0.1:8000/api/auth/logout`(GET) 
