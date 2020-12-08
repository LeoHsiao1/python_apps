# SIMPLEUI_HOME_PAGE = '/admin/'
SIMPLEUI_HOME_ICON = 'fas fa-home'
SIMPLEUI_CONFIG = {
    # 'system_keep': True,
    'menus': [
        {
            'name': '应用一',
            # 'icon': 'fas fa-users',
            'models': [{
                'name': '人物',
                'url': '/admin/app1/person/',
                # 'icon': 'fas fa-users'
            }, {
                'name': '书籍',
                'url': '/admin/app1/book/',
                # 'icon': 'fas fa-user'
            }]
        },
        {
            'name': '站点管理',
            'icon': 'fas fa-cog',
            'models': [{
                'name': '用户',
                'url': '/admin/auth/user/',
                'icon': 'fas fa-user'
            }, {
                'name': '组',
                'url': '/admin/auth/group/',
                'icon': 'fas fa-users'
            }, {
                'name': '日志',
                'url': '/admin/admin/logentry/',
                'icon': 'fas fa-file-alt'
            }]
        },
    ]
}
