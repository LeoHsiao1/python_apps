from django.contrib import admin
from . import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name']


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    # 配置表格页面
    list_display       = ['name', 'author', 'datetime']     # 设置要显示的字段
    list_display_links = ['name']                           # 哪些字段显示成链接，可以跳转到实例的详情页面
    list_filter        = ['datetime']                       # 在页面右侧显示一个过滤器
    search_fields      = ['name', 'author__name']           # 在页面顶部显示一个搜索栏

    # 配置详情页面
    fieldsets = [(None, {'fields':['name', 'abstract', 'author', 'reader_set']})]   # 按顺序显示哪些字段
    autocomplete_fields = ['author']                        # 在哪些外键字段的下拉框中显示一个搜索框以便过滤，实际上是对目标表的 search_fields 进行搜索
    filter_horizontal = ['reader_set']                      # 将哪些 ManyToManyField 字段显示成横向的两个多选框，还会显示搜索框以便过滤
    # filter_vertical = ['reader_set']                      # 与 filter_horizontal 相似，只不过竖向显示
