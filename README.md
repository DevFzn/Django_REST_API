# Django REST API

[Django Rest Framework](https://www.django-rest-framework.org/)

### Requerimientos Rest Framework

- Python (>=3.10)
- Django

<details><summary markdown="span">Opcionales</summary>

- PyYAML, uritemplate: Schema generation support.
- Markdown: Markdown support for the browsable API.
- Pygments: Add syntax highlighting to Markdown processing.
- django-filter: Filtering support.
- django-guardian: Object level permissions support.

</details></br>

### Instalacion

Instalar [requerimientos](./requirements.txt) **en entorno virtual**

```py
pip install -r requirements.txt
```

Django utiliza SQLite3 por defecto para simplificar el desarrolo, en este proyecto
se utliza MariaDB, pero es opcional. Si no requiere sacarlo de
[requirements.txt](./requirements.txt) o desinstalarlo `pip uninstall mysqlclient`

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

## Creación del primer endoint

Creación de endpoint ***Contac***, para que un usuario pueda enviar su *nombre*,
*email*, y *mensaje* al backend.

Para ello se requiere:

- Un modelo que almacene la captura de los datos entrantes.
- Un serializador que procese los datos entrantes del usuario y envíe un
mensaje de respuesta.
- Una vista que encapsule las llamadas a los métodos REST HTTP comunes.
- Una ruta `/url` llamada `/contact/`.


### Model

[./backend/core/models.py](./backend/core/models.py)

Utiliza modelos abstractos del modulo
*django_extensions*; `TimeStampedModel` (campos como *created*), `ActivatorModel`
(campos *status*, *activated date*, *deactivated date* ), `TitleDescriptionModel`
(campos de texto *textfield* y *charfield*).
Clase **Contact** hereda de estos modelos. Todas las tablas del proyecto tendrán
un campo *uuid* como id. Además de un campo *email* de Django. Y método de
representación del modelo en cadena de texto.

**Modelo abstracto**

Para implementar *uuid* en vez de *id* como campo identificador en todos los
modelos, se crea el modulo [model_abstracts.py](./backend/utils/model_abstracts.py)
que hereda de *models* de *django.db* y utliza el campo *id*. Utiliza el campo *UUID*.

### Serializer

Para convertir los datos de entrada *json* en tipos de datos de python, y
viceversa, se crea el archivo [./backend/core/serializers.py](./backend/core/serializers.py)
en la app *core*. Este hereda de la clase *serializers* del modulo *rest_framework*
e implementa sus campos (*CharField* *EmailField*).

### View

[./backend/core/views.py](./backend/core/views.py)
backend
El uso de la clase *APIView* es muy similar al una vista regular, la petición
entrante es enviada a un manejador apropiado para el método, como `.get()` o
`.post()`. Además se pueden establecer otros atributos en la clase que controla
varios aspectos de las normas de la API.

### Route & URL

[./backend/drf_course/urls.py](./backend/drf_course/urls.py)

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

**curl**

```sh
curl -XPOST -H "Content-type: application/json" \
    -d '{"name": "DevFzn", "message": "prueba", "email":"mail@mail.com"}' \
    'http://127.0.0.1:8000/contact/'
```

o **HTTPie**

```sh
http post http://127.0.0.1:8000/contact/ name="DevFzn" message="prueba" \
          email="devfzn@mail.com"
```

<details><summary markdown="span">httpie output</summary>

```http
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

</details>

Se puede utilizar la shell de Django para chequear la nueva entrada en Contact

`./manage.py shell`

```py
>>> from core.models import Contact
>>> c = Contact.objects.last()
>>> c.title
'DevFzn'
```

## Tests

Creación de pruebas en [./backend/core/tests.py](./backend/core/tests.py).
Utilizando las clases `APIClient` que proporciona un cliente incorporado y
`APITestCase`, similar al *TestCase* de Django.

#### Test suite para Contact

0. test setup
1. test ContactViewSet para método create
2. test ContactViewSet para método create cuando nombre no está en los datos
3. test ContactViewSet para método create cuando nombre está en blanco
4. test ContactViewSet para método create cuando mensaje no está en los datos
5. test ContactViewSet para método create cuando mensaje está en blanco
6. test ContactViewSet para método create cuando email no está en los datos
7. test ContactViewSet para método create cuando email está en blanco
8. test ContactViewSet para método create cuando email no es un email

Correr test `./manage.py test`

<details><summary markdown="span">tests output</summary>

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

</details>

## Ecommerce endpoint

Este se compone de 2 endpoints, **items** y **order**. La primera se encarga
de retornar todos los items de la tienda al llamarla, además, si se llama a
este endpoint con una llave primaria, retorna solo ese item. Y cuando se requiera
comprar, se utiliza el *order* endpoint, donde se pasa el item en particular.
Se implementan validaciones para asegurar que el item esten en stock, también
asegurar que solo usuarios autentificado puedan llamar estos endpoints.
Esta app usa *token authentication*. Django Rest Framework facilita esta tarea.

Creación de app *ecommerce*

```py
./manage.py startapp ecommerce
```

Modificar [settings](./backend/drf_course/settings.py) del sitio, editando
`REST_FRAMEWORK` con el siguiente código.
> notar el nuevo `DEFAULT_AUTHENTICATION_CLASSES`.

```py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        ),
    'DEFAULT_AUTHENTICATION_CLASSES': [ # <---
        'rest_framework.authentication.TokenAuthentication', # <---
        ],
    ...
```

Agregar las siguientes apps en `INSTALLED_APPS`.

```py
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken', # <---
    'core',
    'ecommerce', # <---
    ]
```

### URLs

Agregar los nuevos endpoints en [urls.py](./backend/drf_course/urls.py) del sitio.

```py
# importar authtoken
from rest_framework.authtoken.views import obtain_auth_token

# agregar urls
urlpatterns += [
    ...
    path('api-token-auth', obtain_auth_token),
]
```

Cuando un usuario visite este endpoint y pase un nombre de usuario y un password
validos, este recibirá de vuelta un *token* de autentificación. Este token esta
enlazado con el usuario especifico.

Realizar migraciones

```sh
./manage.py makemigrations
./manage.py migrate
```

#### Signals

Se requiere un mecanismo (signal) que cree un token para cada usuario que este registrado
en la app. Este token es el que será devuelto cada vez que se llame al nuevo endopint.

Para ello, crear el archivo [./backend/ecommerce/signals.py](./backend/ecommerce/signals.py).

```py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

> En Django se le llama señal al código que recibe una señal de cierta tabla,
basado en una acción (***pre-save*** o ***post-save***). Cuando se crea un
registro en la tabla, esta envía una señal, y es interceptada por *signals*.
En este caso, se utiliza para generar un nuevo token.


Agregar el siguiente método en la clase `EcommerceConfig` del archivo
[apps.py](./backend/ecommerce/apps.py) de la app.

```py
class EcommerceConfig(AppConfig):
    ...

    def ready(self):
        import ecommerce.signals
```

Creamos otro superusuario, para que se active el disparador de la señal, y se
cree un nuevo token para este.

```sh
./manage.py runserver
./manage.py createsuperuser
```

Visitar [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), y verificar
creación del token.

Probar retorno del token a traves de la API.

ej. **curl**

```sh
curl -XPOST -F 'username=<tu-usuario>' -F 'password=<tu-password>' \
               'http://127.0.0.1:8000/api-token-auth/'
```

ej. **HTTPie**

```sh
http post http://127.0.0.1:8000/api-token-auth/ username=<tu-usuario> \
                                                password=<tu-password>
```

<details><summary markdown="span">httpie output</summary>

```http
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Thu, 29 Mar 2023 11:57:43 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.10.10
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "token": "2f076a6310a244283c6902a73e07a0febc59649c"
}
```

</details>

### Ecommerce Model

Esta app hace uso obligatorio del token de autentificación. Solo usuarios
autentificados pueden acceder a este endpoint.

La app ecommerce se construye con un endpoint **item** y otro **order**. Los
usuarios podrán recuperar elementos de la base de datos, hacer un pedido y
recuperar la información del pedido.

Se necesitan modelos, enrutadores, serializadores y vistas. (models, routers,
serializers & view/sets api/view).

Creación de [modelos](./backend/ecommerce/models.py) Item y Order. Creación
de [serializers](./backend/ecommerce/serializers.py).

Registro de app en el panel de [administración](./backend/ecommerce/admin.py).

Migraciones `./manage.py makemigrations` y `./manage.py migrate`.

### Ecommerce Views y URLs

Creación de [views](./backend/ecommerce/views.py) de la app, se utiliza
`IsAuthenticated` del framework.
Se agrega conjunto de vistas genericas de la app en [urls.py](./backend/drf_course/urls.py)
del sitio, registrandolas en el `router`.

```py
...
from ecommerce import views as ecommerce_views
...

router = routers.DefaultRouter()
router.register(r'item', ecommerce_views.ItemViewSet, basename='item')
router.register(r'order', ecommerce_views.OrderViewSet, basename='order')

...
```

### Ecommerce Tests

Creación de [test](./backend/ecommerce/tests.py) unitarios para la aplicación.

0. test setup
1. test ItemsViewSet método list
2. test ItemsViewSet método retrieve
3. test Item.check_stock cuando order.quantity > item.stock
4. test Item.check_stock cuando order.quantity == item.stock
5. test Item.check_stock cuando order.quantity < item.stock
6. test OrdersViewSet método create cuando order.quantity > item.stock
7. test OrdersViewSet método create cuando order.quantity < item.stock
8. test OrdersViewSet método create cuando order.quantity == item.stock
9. test OrdersViewSet método list
10. test OrdersViewSet método retrieve

Correr tests `./manage.py test`.

<details><summary markdown="span">tests output</summary>

```py
Found 18 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................
----------------------------------------------------------------------
Ran 18 tests in 2.248s

OK
Destroying test database for alias 'default'...
```

</details>

</br>

[Bash script](./api_calls.sh) con llamadas a la API utilizando curl

----

<details><summary markdown="span">Jerarquía de directorios</summary>

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
│   ├── 📂️ ecommerce
│   │   ├── 📂️ migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── 📂️ utils
│   │   ├── __init__.py
│   │   └── model_abstracts.py
│   ├── .env
│   └── manage.py
├── .gitignore
├── api_calls.sh
├── env.template
├── README.md
└── requirements.txt
```

</details>
