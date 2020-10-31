# Развертывание #
```sh
$ docker-compose up -d --build
```

Откройте браузер по ссылке http://localhost:8020

```sh
$ docker-compose exec web /bin/bash
$ python3 manage.py createsuperuser
```

Создаем пользователя с админскими правами.


