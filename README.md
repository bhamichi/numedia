# Update Debian packages
- sudo apt update
- apt list --upgradable
- sudo apt upgrade (if need)

# Uninstall and remove PostgreSQL on Debian Linux (if need)
- sudo apt-get --purge remove postgresql
- sudo apt-get purge postgresql*
- sudo apt-get --purge remove postgresql postgresql-doc postgresql-common
- check: dpkg -l | grep postgres

# Install/configure postgresql (if need)
- sudo apt-get -y install postgresql
- check, should be active: systemctl status postgresql 
- Connect as 'postres' user and set a password: 
    - sudo su - postgres
    - psql
    - ALTER USER postgres PASSWORD 'postgres';
      => you should see in response ALTER ROLE

# Installer pgadmin4 in web mode and configure with apach
- Service appach running? sudo service apache2 status 
- Install: sudo apt install pgadmin4-web
- Configure pgadmin with apach: sudo /usr/pgadmin4/bin/setup-web.sh
- Connect to http://127.0.0.1/pgadmin4/ (with already configured credential)
- Pgadmin4: initiate a new connection into our db
    * right click on servers > register
    * Provide server [name=any], [host=localhost], [Username=postgres] and [passowrd=postgres] ... you should be able to connect 
- Pgadmin4: register new user for our backend application
    * Login/Group Roles > right click and CREATE
    * Give the User [name=numedia_user], [password=numedia_user] and [previlages=Canlogin,CreateDatabase,InheritRight]
- Pgadmin4: create a new db
    * databases > create
    * in General, [name=numedia_db], [Owner=numedia_user] (assign previous created user), then SAVE
    * In schemas > public > tables, you will see no tables have been created

# Github
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
- install pip & virt. env.: sudo apt install python3-venv python3-pip
- create virtual env: python3 -m venv venv
- activate: source venv/bin/activate

# Dependencies
- create under project a file : requirement.txt
    django==4.2
    psycopg2-binary
    django-tenants
    python-decouple
    Pillow
    django-tenant-users
    django-environ
- install (sans sudo): pip install -r requirement.txt
- check for example: django-admin --version

# Porject & Apps
- create project: django-admin startproject project .
- create backend app: python manage.py startapp backend
- create tenants app: python manage.py startapp tenants

# DB Settings
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

# Multi-Tenants Settings
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

# Run Serv
- python manage.py runserver
- http://127.0.0.1:8000/
    * Page not found (404), No tenant for hostname "127.0.0.1"
- http://127.0.0.1:8000/admin
    * Page not found (404), No tenant for hostname "127.0.0.1"
- As workerround, add : SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
    * reference: #https://stackoverflow.com/questions/67221443/show-the-main-page-in-the-django-multi-tenant
    * IMPORTANT: #Temporary for creating 1st public tenant using browser django admin. After creating 1st public tenant, need to remove (or comment) it.
- we need to create a super user for connecting to http://127.0.0.1:8000/admin (only for new created project)
- refer to: https://docs.djangoproject.com/en/1.8/intro/tutorial02/


- http://127.0.0.1:8000/ & http://127.0.0.1:8000/admin are accessible now
- So, we can create a Pucblic Tenant and it's domain URL
- Reset Password via Django Shell: python manage.py shell
    from backend.models import TenantUser
    user = TenantUser.objects.get(email='b.hamichi@gmail.com')
    user.set_password('new_password')
    user.save()
    exit()
    note: Replace 'new_password' and 'email' with the desired

# Create 1st TENANT & DOMAIN
- We need to create a super user for connecting to http://127.0.0.1:8000/admin
    * python manage.py createsuperuser
    * Provide User name and Passwd
    * change password (if need): python manage.py changepassword <username>
    * Then run again the server: you will be able to connect
- create a tenant whose schema is public and it’s address is your domain URL. https://django-tenants.readthedocs.io/en/latest/use.html
    * go to: http://127.0.0.1:8000/admin and create 1st tenant & domain
    a) 1st tenant must be with schema_name='public' : becuase the DB is comes with Schemas(1), which contains only 'public' 
    b) domain = 'localhost' #or your domain url
    c) with domain, need to enter tenant = a)
    d) is_primary = true
- check in 'pgAdmin4' that tenant and his domain were created with success in 'public' schema

# Create 2nd TENANT & DOMAIN
- Create
    * go to: http://127.0.0.1:8000/admin and create a tenant (not public) & his subdomain (or domain)
    * schema_name='tenant1'
    * domain = 'tenant1.domain.com'
- check in 'pgAdmin4' : new schema has been created with name 'tenant1'
- and so on for other tenants
- Check in browser :
    * http://localhost:8000/ : access OK
    * http://tenant1.localhost:8000/ : access OK
    * http://tenant2.localhost:8000/ : access NOK (not created yet)
    * don't forget to comment (or remove) : SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

# Tenants Models
- add models under 'tenants' app
- add admin models under 'tenants' app
- python manage.py makemigrations
- python manage.py migrate_schemas [without --shared]

# Django Tenants Users
* 
les tables USER, GROUP et PERMISSION sont par défaut partagées entre tous les tenants. C'est parce que Django utilise les tables d'authentification de base de données pour tous les utilisateurs, indépendamment du schéma auquel ils appartiennent.
Pour gérer les utilisateurs, groupes et permissions spécifiques à chaque  locataire, vous pouvez utiliser la bibliothèque django-tenant-users
* 

- https://django-tenant-users.readthedocs.io/en/latest/index.html#
- Add 'django-tenant-users' to 'requirement.txt' and install

# COMMIT
- don't forget to make a 1st commit in this stage (?)
