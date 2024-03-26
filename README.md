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
   Создание связи между ошейником и животным, что записывается в таблицу DogsCollars
   
6. **Получение текущих данных об животном**
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
    
14. **Добавление собаки в "Отслеживаемые"**
    Пользователь отправляет запрос на создание "связи" между пользователем и собакой в таблице UsersDogs
    
15.**Удаление собаки из "Отслеживаемых"**
    Пользователь отправляет запрос на удаление "связи" между пользователем и собакой в таблице UsersDogs
    
16.**Получение списка отслеживаемых**
    Пользователь отправляет запрос на получение списка отслеживаемых собак по выборке "связей" из таблицы UsersDogs
    
17. **Получение списка отслеживающих**
    Персонал отправляет запрос на получение списка пользователей, отслеживающих собаку по выборке "связей" из таблицы UsersDogs

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
    "success": false,
    "exception": {
        "message": "Unknown Error"
    }
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
```/collar/register```

+ Request
```
{
    "id":"2311",
    "ip":"122.32.12.33",
    "accessToken": "P9UISH12442KID8"
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
```/dogs/register```

+ Request
```
{
    "name":"Bobik",
    "collar_id":"2311",
    "description":"Black bastard of German Shepherd and mongrel dog",
    "accessToken": "P9UISH12442KID8"
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
```/dogs/status```

+ Request
```
{
    "dog_id":"12",
    "accessToken": "P9UISH12442KID8"
}
```

+ Response
```
{
    "name":"Bobik",
    "collar_id":"2311",
    "description":"Black bastard of German Shepherd and mongrel dog",
    "tasks":[{"id":82},{"id":15},{"id":92}],
    "latitude":"37.23213",
    "longitude":"55.83231",
    "date":"2024-03-26 18:15:00"
}
```

### Getting dog's list
```/dogs/list```

+ Request
```
{
    "accessToken": "P9UISH12442KID8",
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

### Getting dog's data
```/dogs/update```

+ Request
```
{
    "collar_id":"2311",
    "latitude":"37.23213",
    "longitude":"55.83231"
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
```/task/create```

+ Request
```
{
    "dog_id":"12",
    "type":"feed",
    "accessToken": "P9UISH12442KID8"
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
```/task/verify/send```

+ Request
```
{
    "task_id":"82",
    "proof":"Jvch1HJ.png",
    "accessToken": "P9UISH12442KID8"
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

### Getting verify list
```/task/verify/list```

+ Request
```
{
    "accessToken": "P9UISH12442KID8"
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
```/task/update```

+ Request
```
{
    "task_id":"12",
    "status":"complete",
    "accessToken": "P9UISH12442KID8"
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
```/task/verify/refusing```

+ Request
```
{
    "response_id":"81",
    "accessToken": "P9UISH12442KID8"
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
```/task/verify/refusing```

+ Request
```
{
    "response_id":"81",
    "accessToken": "P9UISH12442KID8"
}
```

+ Response
```
{
    "success": true,
    "exception": null,
}
```

### Add to monitor
```/monitor/add```

+ Request
```
{
    "user_id":"81",
    "dog_id":"12",
    "accessToken": "P9UISH12442KID8"
}
```

+ Response
```
{
    "success": true,
    "exception": null,
}
```

### Delete from monitor
```/monitor/delete```

+ Request
```
{
    "user_id":"81",
    "dog_id":"12",
    "accessToken": "P9UISH12442KID8"
}
```

+ Response
```
{
    "success": true,
    "exception": null,
}
```

### List monitoring dogs
```/monitor/dogs```

+ Request
```
{
    "user_id":"81",
    "accessToken": "P9UISH12442KID8"
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

### List monitoring users
```/monitor/users```

+ Request
```
{
    "dog_id":"12",
    "accessToken": "P9UISH12442KID8"
}
```

+ Response
```
{
    "users":[
    {
    "id":"122",
    "nickname":"Valera",
    "email":"valerkin@gmail.com",
    "phone":"727772912"
    },
    {
    "id":"45",
    "nickname":"Pasha",
    "email":"PashaKasha@gmail.com",
    "phone":"88005353535"
    }]
}
```
