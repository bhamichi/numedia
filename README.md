# GITHUB
- in github, go to repository, then code, then copy url clone https
- download git exetnsion in vscode : Source Controle
- click on view Git Graph, then
- click on "Clone Git Repositry"
- note: clone using cmd not working : authentication with cmd (user/passwd) not more used in github
- run :
    * git config --global user.email "you@example.com"
    * git config --global user.name "Your Name"

# PYTHON, PIP, VIRTUEAL-ENV
- keep packages up to date: sudo apt update
- install: sudo apt install python3
- check: python3 --version
- install pip: sudo apt install python3-pip
- install virtual env: sudo apt install python3-virtualenv
- create virtual env: sudo virtualenv -p python3 venv
- activate: ~/venv/bin/ then, source activate

# DEPENDECIES
- create under project a file : requirement.txt
    django
    psycopg2-binary
    django-tenants
    python-decouple
- install (sans sudo): pip install -r requirement.txt
- check for example: django-admin --version

# PROJECT & APPs
- create project: django-admin startproject project .
- create backend app: python manage.py startapp backend
- create tenants app: python manage.py startapp tenants

# DB SEETINGS
- Prerequisite: the db (ex. numedia) must be created before
- Create .env file by adding :
    DB_NAME=numedia
    DB_USER=postgres_user
    DB_PASSWORD=postgres_passwd
    DB_HOST=localhost
    DB_PORT=5432
- Configure DB: project/seeting.py
    - from decouple import config
    - DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
            }
        }

# SEETINGS MULTI-TENANTS
- referto url: https://django-tenants.readthedocs.io/en/latest/install.html
- Here how shared and tennant apps are configured
    SHARED_APPS = (
        'django_tenants',  # mandatory
        'backend', # you must list the app where your tenant model resides in

        # everything below here is optional
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    TENANT_APPS = (
        # your tenant-specific apps
        'tenants',
    )

    TENANT_MODEL = "backend.Client" # app.Model

    TENANT_DOMAIN_MODEL = "backend.Domain"  # app.Model

- python manage.py makemigrations
- python manage.py migrate_schemas --shared
    * this will create two additional tables on shared (backend) 
        backend_client
        backend_domain

# RUN SERV
- python manage.py runserver
- http://127.0.0.1:8000/
    * Page not found (404), No tenant for hostname "127.0.0.1"
- http://127.0.0.1:8000/admin
    * Page not found (404), No tenant for hostname "127.0.0.1"
- As workerround, add : SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
    * reference: #https://stackoverflow.com/questions/67221443/show-the-main-page-in-the-django-multi-tenant
- http://127.0.0.1:8000/ & http://127.0.0.1:8000/admin are accessible now
- So, we can create a Pucblic Tenant and it's domain URL

# CREATE TENANT & DOMAIN
- create a tenant whose schema is public and it’s address is your domain URL. https://django-tenants.readthedocs.io/en/latest/use.html
    * create: http://127.0.0.1:8000/admin
    * 1st tenant must be with schema_name='public'
- We need to create a super user for connecting
    * python manage.py createsuperuser
    * Provide User name and Passwd
    * Then run again the server: you will be able to connect
    * change password : python manage.py changepassword <username>

# COMMIT
- don't forget to make a 1st commit in this stage (?)

