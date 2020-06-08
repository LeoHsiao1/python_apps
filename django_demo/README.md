# django_demo

这是一份示例代码，方便建立新的 Django 项目。
- django_sample/settings.py 中的 SECRET_KEY 要重新生成。
- 数据库采用 SQLite ，但可以在 django_sample/settings.py 中切换成 MySQL 。

初始化：
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

启动：
```sh
python manage.py runserver 0.0.0.0:8000
```
