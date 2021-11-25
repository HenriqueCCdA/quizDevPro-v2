# 🐍 QuizDevPro-v2 🐍

![](https://img.shields.io/github/last-commit/HenriqueCCdA/quizDevPro-v2?style=plasti&ccolor=blue)
![](https://img.shields.io/badge/Autor-Henrique%20C%20C%20de%20Andrade-blue)
[![Updates](https://pyup.io/repos/github/HenriqueCCdA/quizDevPro-v2/shield.svg)](https://pyup.io/repos/github/HenriqueCCdA/quizDevPro-v2/)
[![codecov](https://codecov.io/gh/HenriqueCCdA/quizDevPro-v2/branch/main/graph/badge.svg?token=8U5Z5LSRJ0)](https://codecov.io/gh/HenriqueCCdA/quizDevPro-v2)
[![Python application](https://github.com/HenriqueCCdA/quizDevPro-v2/actions/workflows/buid_test_ci.yml/badge.svg)](https://github.com/HenriqueCCdA/quizDevPro-v2/actions/workflows/buid_test_ci.yml)

Nesse repositorio temos o projeto desenvolvido no BootCamp Dev Pro da [PythonPro](www.python.pro.br). O objetivo desse projeto é desenvolver um redutor de url. O link para o deploy da aplicação no **Heroku** pode ser encontrada no link abaixo:

🔥🔥🔥[https://quizdevprov2.herokuapp.com/](https://quizdevprov2.herokuapp.com//)🔥🔥🔥



## Principais tecnologias utilizadas:

Necessidade                   | Tecnologias
---------                     | ------
Framework backEnd             | Django
Framework FrontEnd            | Chart.js
CI                            | Github Actions
CD                            | Heroku
Banco de dados                | PostgresSQL
Gestão de dependecias         | Pipenv
Testes                        | Pytest
Relatorio de Erros            | Sentry
Servidor de arquivo estaticos | Whitenose
WSGI                          | Gunicorn




---

## Passos desensolvidos durante o projeto

### 1) Configuração do projeto 🛠

* Criando o arquivo .gitignore

* criar o ambiente virtual:

   ```console
   python -m venv .venv
   ```
* instalando o gerenciador de dependecias

   ```console
   python -m pip install pip-tools
   ```

* Instalando as dependencias do projeto:

    ```console 
    django
    dj-database-url
    python-decouple
    ipython
    django-extensions 
    psycopg2-binary # opcional
    sentry-sdk
    gunicorn
    whitenoise
    ```

* Instalando as dependencias de desenvolvimento:

    ```console 
    model-bakery
    flake8
    pytest-django
    pytest-cov
    codecov
    django-debug-toolbar
    ``` 

* gerando e instalando as dependecias de desenvolmineto
  ```
  pip-compile requirements.in
  pip install -r requirements.txt
  pip-compile requirements-dev.in
  pip install -r requirements-dev.txt
  ```

* Configurando o flake8 através do arquivo .flake8

   ```yml
   [flake8]
   max-line-length = 120
   exclude=.venv
   ```

* Inicializando o projeto **Django**

   ```console
   pipenv shell
   django-admin.exe startproject quiz .
   ```

  Para testar pode-se rodar o servidor através de:

  ```console
  python manage.py runserver
  ```

* Criando o arquivo local .env e arquivo contrib/env-sample

  ```yml
  DEBUG=FALSE
  SECRET_KEY=Defina sua chave secreta aqui
  ALLOWED_HOSTS=
  INTERNAL_IPS=
  SENTRY_DSN=
  DATABASE_URL=postgres://postgres:postgres@localhost/testedb
  ```

* Configurando o **PyUp** pelo arquivo **.pyup.yml**

    ```yml
    schedule: ''
    update: false
    ```
  
* Configura o codecov pelo arquivo **.codecov.yml**

  ```yml
  coverage:
    status:
      project:
        default:
          # basic
          target: 0%
      patch:
        default:
          # basic
          target: 0%
  ```

* Configurando o pytest-django

  criar o arquivo pytest.in

  ```yml
  [pytest]
  DJANGO_SETTINGS_MODULE = devpro.settings
  ```

  Rodando os testes.

    ```console
    python -m pytest
    ```

* Configurando o **CI**.
  > Link para o GitHub Actions [file](https://github.com/HenriqueCCdA/quizDevPro-v2/tree/main/.github/workflows)

* Criando o usuario costumizado:

  O código base foi retirado da classe AbstracticUser e UserManager encontrado no módulo django.contib.auth.models.py. Criar a varialvel no settings.py

  ```python
  AUTH_USER_MODEL='quiz.encutador'
  ```
    
  Para testa posse usar o makemigrations

  ```console
  python manage.py makemigrations
  ```


* Instalando o ipython e django-extensions

    ```python
    INSTALLED_APPS = [
    ... 
    'django_extensions'    
    ]
    ```

* Instalando django debug toolbar

  Precisa da tabela de usuarios. Por isso tem que se feita depois do migrate 

  Adicionar o código abaixo no arquivo settings.py

    ```python
    INTERNAL_IPS = config('INTERNAL_IPS', cast=Csv(), default=None)

    if DEBUG:
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    ```

  Adicionar o codigo abaixo no arquivo url.py do projeto

    ```python
    if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    ```

* Configurando a coleta dos arquivos estáticos:

    ```python
    STATIC_ROOT = BASE_DIR / 'staticfiles/'
    ```

* Servindo os arquivos estaticos com  o **whitenose**:

    ```console
    pipenv install whitenose
    ```
  ```python
  MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  # ...
   ]
  ```


* Instalando o sentry:

  Configurando o **SENTRY_DSN** no heroku:

    ```console
    heroku config:set SENTRY_DSN="https://asdasdasdsad"
    ```

* Criar a aplicação **base**

  ```console
  cd devpro
  python ..\manage.py startapp base
  ```


### 2) Deploy no heroku 🛠

* Criando o aquivo Procfile:

    ```yml
    release: python manage.py migrate --noinput
    web: gunicorn devpro.wsgi --log-file -
    ```

* Criando apps pelo heroku-cli:

    ```console
    heroku apps:create urlreduce
    ```
    
    Configuração para testar o deploy inicial
   
    ```console
    heroku config:set DISABLE_COLLECTSTATIC=1
    ```
* Testando do deploy no heroku:

   ```console
   git push heroku branch_local:master
   ```

* Configuração para o Deploy automatico é feita no site.

* Configurando o postgres



* Chave gerando a chave secreta para heroku:

    ```console
    >>>from django.core.management.utils import get_random_secret_key
    >>>get_random_secret_key()
    ```

* Configurando as variaveis no heroku:

    ```console
    heroku config:set DEBUG=False
    heroku config:set SECRET_KEY="chave secreta de verdade"
    ```




### 3) Iniciando o projeto 🛠



### 4) Modelo de Dados Final 🛠

![Modelo](./models.svg)
