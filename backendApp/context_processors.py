def function_menu(request):
    function_menu = [
        {
            'name': '首頁',
            'permission': ['admin', 'caregiver', 'pharmacy'],
            'mode': 'one',
            'url': 'index',
            'icon': 'fas fa-home'
        },
        {
            'name': '用戶管理',
            'permission': ['admin'],
            'mode': 'one',
            'url': 'user_manager',
            'icon': 'fa-user-nurse'
        },
        {
            'name': '藥物配送管理',
            'permission': ['pharmacy'],
            'mode': 'one',
            'url': 'medicine_order',
            'icon': 'fa-user-nurse'
        },
        {
            'name': '基本功能',
            'id': 'basicFunctionsMenu',
            'permission': ['caregiver'],
            'mode': 'multi',
            'items': [
                {'url': 'patient_manager', 'name': '被照護者管理', 'icon': 'fa-hospital-user'},
                {'url': 'bed_manager', 'name': ' 床位管理', 'icon': 'fa-solid fa-bed'}
            ]
        },
        {
            'name': '訂單管理功能',
            'id': 'mealsFunctionsMenu',
            'permission': ['caregiver'],
            'mode': 'multi',
            'items': [
                {'url': 'course_order', 'name': '餐點配送管理', 'icon': 'fa-burger'},
                {'url': 'main_course', 'name': '餐點管理', 'icon': 'fa-burger'},
                {'url': 'bom_settings', 'name': '餐點配菜管理', 'icon': 'fa-solid fa-egg'},

            ]
        },
        {
            'name': '進銷存管理功能',
            'id': 'stockFunctionsMenu',
            'permission': ['caregiver'],
            'mode': 'multi',
            'items': [
                {'url': 'inventory_management', 'name': '配菜管理', 'icon': 'fa-solid fa-box-open'},
                {'url': 'purchase_detail', 'name': '配菜進貨管理', 'icon': 'fa-solid fa-cart-flatbed'},
                {'url': 'suppliers', 'name': '配菜供應商管理', 'icon': 'fa-solid fa-city'},
            ]
        }
    ]
    return {'function_menu': function_menu}