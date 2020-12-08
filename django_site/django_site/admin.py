from django.contrib import admin
from import_export.admin import ImportExportMixin


admin.site.site_title  = '后台管理'
admin.site.site_header = admin.site.site_title


class MyModelAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = 15


class MyImportExportModelAdmin(ImportExportMixin, MyModelAdmin):
    pass


@admin.register(admin.models.LogEntry)
class LogEntryAdmin(MyImportExportModelAdmin):
    """ 该类用于显示 admin 内置的 django_admin_log 表 """
    list_display       = ['action_time', 'user', 'content_type', '__str__']   # content_type 是指用户修改的 Model 名
    list_display_links = ['action_time']
    list_filter        = ['action_time', 'content_type', 'user']
    readonly_fields    = ['action_time', 'user', 'content_type',
                          'object_id', 'object_repr', 'action_flag', 'change_message']

