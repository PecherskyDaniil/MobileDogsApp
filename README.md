# MobileDogsApp
**Идея проекта**
  Проект представляет собой систему, состоящую из "умных ошейников", отслеживающих состояние бездомных собак, мобильного приложения, позовляющего пользователям наблюдать за собаками и координировать действия по взаимодействию с ними и сервера, обрабатывающего данные с ошейников и приложения, и связывающего их. Для обработки запросов будет использоваться FastAPI, структуру и код которого содержит данный репозиторий.


**Сценарии:**

1. **Регистрация пользователя**
  Пользователь указывает в запросе имя, фамилию, почту, пароль и номер телефона, из которых (или независимо) которые записываются в таблицу Users (пароль хешируется)

2. **Авторизация пользователя**
  Пользователь указывает в запросе почту и пароль и получает API ключ

3. **Регистрация ошейника**
   Персонал указывает номер и характеристики ошейника(например ip) и он записывается в таблицу Collars
   
4. **Регистрация животного**
   Персонал указывает кличку и описание собаки, которые записываются в таблицу Dogs
   
5. **"Привязка" ошейника к животному**
   Создание связи между ошейником и животным
   
6. **Получение данных об животном**
    Запрос на получение данных по id собаки. В запросе указывается api пользователя и id собаки
    
7. **Получение списка животных (возможен фильтр по местоположению, т.е. вывод ближайших животных)**
    Запрос на получение списка животных, с функцией выборки по координатам. В запросе указывается api пользователя и координаты (опционально)
    
8. **Отправка текущих данных на сервер**
    Отправка координат ошейником на сервер и запись их в таблицу DogsData
    
9. **Создание и привязка "задания" к животному**
    Пользователь отправляет запрос на сервер с типом задания, id собаки и api пользователя для записи в таблицу Tasks
    
10. **Отправка задания на верификацию**
    Пользователь отправляет запрос на сервер с id задания и фото для записи ответа в таблицу TasksResponses
    
11. **Получение списка заданий на верификацию**
    Персонал отправляет запрос на сервер и получает список заданий на верификацию
    
12. **Обновление статуса задания**
    Персонал отправлет запрос с id задания и статусом, который записывается в соответсвующую колонку таблицы Tasks
    
13. **Отклонение ответа на задание**
    Персонал отправлет запрос с id ответа на задание для удаления этого ответа из таблицы TasksResponses
    


**Реализованные запросы**:
## Base Response Format

+ Success

```
{
    "success": true,
    "exception": null
}
```

+ Error
```
{
    "detail": "Unknown Error"
}
```

### User registration
```/user/register```

+ Request
```
{
    "nickname":"Pasha",
    "email":"PashaKasha@gmail.com",
    "phone":"88005353535"
    "password":"qwertyuiop123"
}
```

+ Response
```
{
    "nickname":"Pasha",
    "accessToken": "P9UISH12442KID8"
}
```

### User authorization
```/user/login```

+ Request
```
{
    "nickname":"Pasha",
    "password":"qwertyuiop123"
}
```

+ Response
```
{
    "nickname":"Pasha",
    "accessToken": "P9UISH12442KID8"
}
```

### Collar registration
```/collar/register?token=P9UISH12442KID8```

+ Request
```
{
    "id":"2311",
    "ip":"122.32.12.33",
}
```

+ Response
```
{
    "success": true,
    "exception": null
}
```

### Dog registration
```/dogs/register?token=P9UISH12442KID8```

+ Request
```
{
    "name":"Bobik",
    "collar_id":"2311",
    "description":"Black bastard of German Shepherd and mongrel dog",
}
```

+ Response
```
{
    "success": true,
    "exception": null,
    "dog_id":"12"
}
```

### Getting dog's status
```/dogs/{dogs_id}/data?token=P9UISH12442KID8```

+ Request
```
{
    "dog_id":"12"
}
```

+ Response
```
{
    "name":"Bobik",
    "collar_id":"2311",
    "description":"Black bastard of German Shepherd and mongrel dog",
    "tasks":[...],
    "latitude":"37.23213",
    "longitude":"55.83231",
    "date":"2024-03-26 18:15:00"
}
```

### Getting dog's list
```/dogs?token=P9UISH12442KID8```

+ Request
```
{
    "latitude":"37.23213",
    "longitude":"55.83231",
    "radius":1000
}
```

+ Response
```
{
    "dogs":[
    {
    "id":"12",
    "name":"Bobik",
    "collar_id":"2311"
    },
    {
    "id":"8",
    "name":"Sharik",
    "collar_id":"7365"
    }]
}
```

### Setting dog's data
```/dogs/{dog_id}/data/?token=P9UISH12442KID8&ip=127.0.0.1```

+ Request
```
{
    "latitude":"37.23213",
    "longitude":"55.83231",
    "datetime":"29-04-2024T18:00:00"
}
```

+ Response
```
{
    "success": true,
    "exception": null,
    "dog_id":"12"
}
```

### Create task
```/task/create?token=P9UISH12442KID8```

+ Request
```
{
    "dog_id":"12",
    "type":"feed"
}
```

+ Response
```
{
    "success": true,
    "exception": null,
    "task_id":"82"
}
```

### Send to verify task
```/task/{task_id}/reponses/send?token=P9UISH12442KID8```

+ Request
```
{
    "proof":"Jvch1HJ.png"
}
```

+ Response
```
{
    "success": true,
    "task_id":"82"
}
```

### Getting verify list
```/task/{task_id}/responses?token=P9UISH12442KID8```

+ Request
```
{
}
```

+ Response
```
{
    "tasks":[
      {
        "response_id":"33",
        "task_id":"82",
        "proof":"Jvch1HJ.png",
        "user_id":"22"
      },
      {
        "response_id":"81",
        "task_id":"73",
        "proof":"OlyeD1P.png",
        "user_id":"15"
      }
    ]
}
```

### Task status update
```/task/{task_id}/change_status?token=P9UISH12442KID8```

+ Request
```
{
    "status":1
}
```

+ Response
```
{
    "success": true,
    "exception": null,
}
```

### Response delete
```/task/responses/{response_id}/delete?token=P9UISH12442KID8```

+ Request
```
{
}
```

+ Response
```
{
    "success": true,
    "exception": null,
}
```
### Запуск приложения
Для работы приложения установите следующие библиотеки:

1. sqlalchemy
```
pip install sqlalchemy
```
2. fastapi
```
pip install fastapi
```
После установки библиотек можно запустить приложение. Находясь в основной папке проекта запустите следующую команду:
```
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
Для запуска тестов установите pytest и запустите в основной папке. Учтите что возможно придется запустить pytest дважды, поэтому не пугайтесь если после первого запуска вам выдаст ошибку.

https://mobiledogsapp.readthedocs.io/ru/main/


# Отправка логов на elastic с помощью filebeat
![Чудо ELK](https://github.com/PecherskyDaniil/MobileDogsApp/assets/81502368/8f545986-b602-448f-bb97-069aa63719ce)

