# BB Product / Popuplation
BB Product / Population is used for export/import data from CSV file to database and vice versa
## Installation
Use the package manager [pipenv](https:https://pypi.org/project/pipenv/) to install requirements.
```bash
pipenv install
```
## Migrations
Use migrate command to create database tables using 
```bash
python manage.py migrate
```
Create superuser using
```bash
python manage.py createsuperuser
```
**make sure to select the user role on database.**
## Run Project
Run the server on any port you want by default it can access using below
```bash
python manage.py runserver
```
## Usage
Login to the system with
```bash
http://127.0.0.1:8000/login/
```
## Note
Schema for models Population and BB Product can be scene in file named as **schema.txt** and UML class diagram can also be seen with the name **data_assessment_models.png**
