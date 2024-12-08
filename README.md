FSP проект
-
Используется postrgesql
Для запуска создайте bd postgress и установите prod requirements.
Добавьте ```.env``` в ```FSP_jestkie_programisty``` и добавьте туда поля NAME=name, USER=user, PASSWORD=passw
проипишите
```commandline
python3 manage.py makemigrations
python3 manage.py migrate
```
![JPG IMAGE](ER.jpg)
для парсинга есть url parse/
по url/login auth доступен вход
и других
Для загрузки фикстур ```python manage.py loaddata fixtures/data.json ```
логин главному админу
admin_1
пароль
admin
Презентция: 'ФСП_Презинтация.pdf'
добавьте поля для почты
в .end
EMAIL = <Ваш email>
EMAIL_PASSWORD = <pw>