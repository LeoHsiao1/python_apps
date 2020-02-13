from django.contrib import admin
from django.urls import path, include
# from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')), # 转发给 app1 的 urls.py
]
