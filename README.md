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
```

Django utiliza SQLite3 por defecto facilitar el desarrolo, en este proyecto se
utliza MariaDB, pero es opcional.

```py
pip install mysqlclient
```

## Inicio del proyecto

**Creación del proyecto Django**

```sh
mkdir backend
django-admin startproject drf_course backend
```

Este proyecto consta de 2 aplicaciones.

La primera es el núcleo. Esta contendrá la lógica del contacto con el *endpoint*.
La segunda será *ecommerce*. Esta contendrá la ĺógica del endpoint de los
*items* y ordenes.

```sh
cd backend
./manage.py startapp core
```

### Editar configuración del proyecto

Archivo [./backend/drf_course/settings.py](./backend/drf_course/settings.py).

Importar variables de entorno usando *python-dotenv* del archivo en `.backend/.env`.

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
las variables de entorno declaradas en `./backend/.env`

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

#### Migrar y probar aplicación

```sh
./manage.py migrate
./manage.py runserver
```

### Creación del primer endoint

Creación de endpoint de ***contacto***, para que un usuario pueda enviar su
*nombre*, *email*, y *mensaje* al backend.

Para ello se requiere:

- Un modelo que almacene la captura de los datos entrantes.
- Un serializador que procese los datos entrantes del usuario y envíe un
mensaje de respuesta.
- Una vista que encapsule las llamadas a los métodos REST HTTP comunes.
- Una ruta `/url` llamada `/contact/`.


#### Model

[./backend/core/models.py](./backend/core/models.py)

Utiliza modelos abstractos del modulo
*django_extensions*; `TimeStampedModel` (campos como *created*), `ActivatorModel`
(campos *status*, *activated date*, *deactivated date* ), `TitleDescriptionModel`
(campos de texto *textfield* y *charfield*).
Clase **Contact** hereda de estos modelos. Todas las tablas del proyecto tendrán
un campo *uuid* como campo id. Además de un campo *email* de Django. Y método de
representación del modelo en cadena de texto.

**Modelo abstracto**

Para implementar *uuid* en vez de *id* como campo identificador en todos los
modelos, se crea el modulo [model_abstracts.py](./backend/utils/model_abstracts.py)
que hereda de *models* de *django.db* y utliza el campo *id*. Utiliza el campo *UUID*.

#### Serializer

Para convertir los datos de entrada *json* en tipos de datos de python, y
viceversa, se crea el archivo [./backend/core/serializer.py](./backend/core/serializer.py)
en la app *core*. Este hereda de la clase *serializers* del modulo *rest_framework*
e implementa sus campos (*CharField* *EmailField*).

#### View

[./backend/core/views.py](./backend/core/views.py)

El uso de la clase *APIView* es muy similar al una vista regular, la petición
entrante es enviada a un manejador apropiado para el método, como `.get()` o
`.post()`. Además se pueden establecer otros atributos en la clase que controla
varios aspectos de las normas de la API.

#### Route & URL

[./drf_course/urls.py](./drf_course/urls.py)

El framework REST añade soporte para ruteo automático de URLs a Django y provee
al programador de una simple, rápida y consistente forma de enlazar la lógica
de la vista a un conjunto de URLs.

#### Registrar app en panel de administración

Importar modelo y registrar en [./backend/core/admin.py](./backend/core/admin.py).

Crear las migraciones y migrar.

```py
./manage.py makemigrations
./manage.py migrate
```
Finalmente, crear **super usuario**.

```py
./manage.py createsuperuser
```

#### Prueba manual

**Curl**

```sh
curl -XPOST -H "Content-type: application/json" \
    -d '{"name": "DevFzn", "message": "prueba", "email":"mail@mail.com"}' \
    'http://127.0.0.1:8000/contact/'
```

o **Httpie**

```sh
http post http://127.0.0.1:8000/contact/ name="DevFzn" message="prueba" \
          email="devfzn@mail.com"
```

```sh
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 155
Content-Type: application/vnd.api+json
Cross-Origin-Opener-Policy: same-origin
Date: Wed, 29 Mar 2023 20:05:32 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.10.10
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "data": {
        "attributes": {
            "email": "devfzn@mail.com",
            "message": "prueba",
            "name": "DevFzn"
        },
        "id": "bef5e90c-821a-4d04-98ef-c0a0adde5ec1",
        "type": "ContactAPIView"
    }
}
```

Se puede utilizar la shell de Django para chequear la nueva entrada en Contacto

`./manage.py shell`

```py
>>> from core.models import Contact
>>> c = Contact.objects.last()
>>> c.title
'DevFzn'
```

#### Jerarquia de directorios

```txt
📂️ .
├── 📂️ backend
│   ├── 📂️ core
│   │   ├── 📂️ migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── 📂️ drf_course
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── 📂️ utils
│   │   ├── __init__.py
│   │   └── model_abstracts.py
│   ├── .env
│   └── manage.py
├── .gitignore
├── env.template
├── README.md
└── requirements.txt
```

## Tests

Creación de pruebas en [./backend/core/tests.py](./backend/core/tests.py).
Utilizando las clases `APIClient` que proporciona un cliente incorporado y
`APITestCase`, similar al *TestCase* de Django

#### Test suite para Contact

0. SetUp de los test
1. test ContactViewSet método create
2. test ContactViewSet método create cuando nombre no está en los datos
3. test ContactViewSet método create cuando nombre está en blanco
4. test ContactViewSet método create cuando mensaje no está en los datos
5. test ContactViewSet método create cuando mensaje está en blanco
6. test ContactViewSet método create cuando email no está en los datos
7. test ContactViewSet método create cuando email está en blanco
8. test ContactViewSet método create cuando email no es un email

Correr test `./manage.py test`

```py
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 0.028s

OK
Destroying test database for alias 'default'...
```

