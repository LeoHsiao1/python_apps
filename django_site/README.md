# django_site

这是一份示例代码，方便建立新的 Django 项目。
- 部署之前，需要重新生成 django_sample/settings.py 中的 SECRET_KEY 。
- 数据库采用 SQLite ，可以在 django_sample/settings.py 中切换成 MySQL 。
- 采用 django-simpleui 显示后台管理页面。

## 部署

1. 安装 Python3 
2. 安装依赖：
    ```sh
    pip install -r requirements.txt
    ```
3. 初始化数据库：
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```
4. 启动服务器：
    ```sh
    python manage.py runserver 0.0.0.0:80
    ```
    访问 <http://127.0.0.1:80/admin/> 即可使用后台管理页面。
