# CompSecProj2020-backend
# Backend Requirements
in your virtual environment, run the following commands

python -m pip install Django\
pip install djangorestframework\
pip install djangorestframework-simplejwt\
pip install django-cors-header

## How to sync Database
Run\
python manage.py makemigrations\
python manage.py migrate

## To run a development server
Run\
python manage.py runserver

## To create superuser that can login to localhost/admin
python manage.py createsuperuser