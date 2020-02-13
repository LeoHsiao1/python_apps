from django.contrib import admin
from . import models

admin.site.site_title = '网站标题'
admin.site.site_header = '网站标题'


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'datetime']  # 设置要显示的字段
    list_display_links = ['name']  # 点击哪些字段可以链接到实例的修改页面
    list_filter = ['datetime']  # 在页面右侧显示一个过滤器
    search_fields = ['name']  # 在页面顶部显示一个搜索栏

    # 定义实例修改页面的排版
    fieldsets = [(None, {'fields': ['name', 'product']}),
                 ('配置', {'fields': ['configs']})
                 ]

    actions = ['action1']  # 一个列表，包含自定义的actions

    def action1(self, request, queryset):  # 定义一个动作
        try:
            for project in queryset:
                # do something
                pass
            self.message_user(request, 'done')
        except Exception as e:
            self.message_user(request, e)

    action1.short_description = '动作1'
