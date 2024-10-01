# Онлайн выставка котят

Это REST API для онлайн выставки котят, разработанное с использованием Django и Django REST Framework. API позволяет пользователям управлять информацией о котятах, оценивать их и аутентифицироваться с помощью JWT.

## Стек технологий

- **Backend**: Django, Django REST Framework
- **База данных**: SQLite
- **Аутентификация**: JWT

## Эндпоинты API

   - Получение списка пород: GET /breeds/
   - Получение списка всех котят: GET /kittens/
   - Получение списка котят определенной породы: GET /kittens/?breed=<breed_name>
   - Получение подробной информации о котенке: GET /kittens/<kitten_id>/
   - Добавление котенка: POST /kittens/
   - Изменение информации о котенке: PUT /kittens/<kitten_id>/
   - Удаление котенка: DELETE /kittens/<kitten_id>/
   - JWT Авторизация пользователей: POST /auth/token/

     доп:
     - Эндпоинт для получения котят по цвету GET /kittens/by-color?color=<color_name>
## Документация

   - API документирован с помощью Swagger. Доступ к документации можно получить по адресу:
    ```http://127.0.0.1:8000/swagger/```

## Установка

1. **Клонируйте репозиторий**:
   ```
   git clone https://github.com/pavlowave/workmate_test.git
   cd workmate_test
   ```
2. **Создайте и активируйте виртуальное окружение**:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте: venv\Scripts\activate
   ```
3. **Установите зависимости**:
   ```
   pip install -r requirements.txt
   ```
4. **Создаем .env**:
   Перейдите в рабочую директорию:
   ```
   cd backend
   ```
5. **Создаем БД:**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   Создаем пользователя для админки:
   ```
   python manage.py createsuperuser
   ```
   
   
## Использование Django Shell для создания пользователя и пород котят
   ```
   python manage.py shell
   ```
 в Django Shell:
 ```
from django.contrib.auth.models import User
from pets.models import Breed
from rest_framework_simplejwt.tokens import RefreshToken
```
Создание пользователя
```
user = User.objects.create_user(username='kittenlover', password='kittenpassword')
```
 Генерация JWT токена для конкретного пользователя
```
refresh = RefreshToken.for_user(user)
token_data = {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
}
```
 Создание пород
```
breed1 = Breed.objects.create(name='Siamese')
breed2 = Breed.objects.create(name='Persian')
breed3 = Breed.objects.create(name='Maine Coon')
```
 Проверка созданных объектов
```
print(User.objects.all())
print(Breed.objects.all())
```
 Печать токенов только для созданного пользователя
```
print(f"Tokens for user '{user.username}':")
print("Refresh Token:", token_data['refresh'])
print("Access Token:", token_data['access'])
```
  Реализовал сигнал, который создает еще один токен автоматом и показывает его. Время жизни токена установлено 60 минут, для более удобного тестирования(настраиваестя в settings.py проекта)
  С помощью токена можно протестировать api в ```http://127.0.0.1:8000/swagger/```. В настрйоках настроены SECURITY_DEFINITIONS в SWAGGER_SETTINGS.

## Минимальные данные для тестирования

Для добавления котенка, необходимо передать:
```
{
    "breed": 1,
    "color": "Белый",
    "age_months": 3,
    "description": "Милый и игривый котенок."
}
```

## Дополнительные возможности
- Оценка котят: Каждый пользователь может оценивать котят один раз(от 1 до 5). Не аутентифицированные могут просто видеть оценки котят. Есть средняя оценка.
- Тестирование: Написаны тесты с использованием pytest для проверки работоспособности функций API. Для запуска тестов используйте:
  ```
  pytest
  ```

## Автор
Павел Сидоров
