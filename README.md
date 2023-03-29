# Django REST API

[Django Rest Framework](https://www.django-rest-framework.org/)

### Requerimientos Rest Framework

- Python (>=3.10)
- Django

Optional:

- PyYAML, uritemplate: Schema generation support.
- Markdown: Markdown support for the browsable API.
- Pygments: Add syntax highlighting to Markdown processing.
- django-filter: Filtering support.
- django-guardian: Object level permissions support.

**En entorno virtual**

```py
pip install djangorestframework
```

### Instalacion

```py
pip install django-extensions djangorestframework djangorestframework-jsonapi \
inflection python-dotenv sqlparse

Django utiliza SQLite3 por defecto facilitar el desarrolo, en este proyecto se
utliza MariaDB, pero es opcional.

# MariaDB
pip install mysqlclient
```

### Inicio del proyecto

```sh
mkdir backend

# Creación del proyecto Django
django-admin startproject drf_course backend
```

Este proyecto consta de 2 aplicaciones.

La primera es el núcleo. Esta contendrá la lógica del contacto con el *endpoint*.
La segunda será *ecommerce*. Esta contendrá la ĺógica del endpoint de los
*items* y ordenes.

```sh
cd backend
python manage.py startapp core
```

### Editar configuración del proyecto

Archivo [./backend/drf_course/settings.py](./backend/drf_course/settings.py).

Importar `.env` usando *python-dotenv*.

```py
from dotenv import load_dotenv
import os

load_dotenv()
```

Reemplazar `ALLOWED_HOSTS`, `SECRET_KEY` y `DEBUG`.

```py
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
```

Añadir aplicaciones
```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', # <---
    'django_filters', # <---
    'rest_framework', # <---
    'core', # <---
]

```

Añadir variables del framework REST al final del arhivo.

```py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework_json_api.filters.SearchFilter',
        ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}
```

En caso de utilizar MariaDB, cambiar la declaración de *DATABASES*, para usar
las variables de entorno declaradas en [./backend/env](./backend/.env)

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("MARIADB_DBASE"),
        'USER': os.environ.get("MARIADB_USER"),
        'PASSWORD': os.environ.get("MARIADB_PASS"),
        'HOST': os.environ.get("MARIADB_HOST"),
        'PORT': os.environ.get("MARIADB_PORT"),
    }
}
```

Modificar [./backend/drf_course/urls.py](./backend/drf_course/urls.py)

```py
from django.contrib import admin
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]
```

