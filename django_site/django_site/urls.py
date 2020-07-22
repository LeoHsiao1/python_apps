from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),
]


admin.site.site_title = '后台管理'
admin.site.site_header = '后台管理'
