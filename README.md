# FastApi-JWT

Структура папок

FastApi-JWT
│   .env
│   alembic.ini
│   base.db
│   file.txt
│   main.py
│   output.txt
│   README.md
│
├───config
│       env.py
│       __init__.py
│
├───migrations
│   │   env.py
│   │   README
│   │   script.py.mako
│   │
│   └───versions
│           5dd13d09c19d_init.py
│
└───src
    │   __init__.py
    │
    ├───auth
    │       schemas.py
    │       security.py
    │
    ├───core
    │       exception.py
    │       response.py
    │       serializer.py
    │       __init__.py
    │
    ├───database
    │       manager.py
    │       model.py
    │       _abcrepos.py
    │       __init__.py
    │
    ├───routers
    │   │   __init__.py
    │   │
    │   ├───auth
    │   │       repos.py
    │   │       router.py
    │   │       schemas.py
    │   │
    │   └───user
    │           depends.py
    │           repos.py
    │           router.py
    │           schemas.py
    │
    └───scopes
            scopes.py
