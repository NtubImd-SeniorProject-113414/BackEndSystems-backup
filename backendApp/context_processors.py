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
            'icon': 'fa-solid fa-vr-cardboard',
            'mode': 'multi',
            'items': [
                {'url': 'patient_manager', 'name': '被照護者管理', 'icon': 'fa-hospital-user'},
                {'url': 'bed_manager', 'name': ' 床位管理', 'icon': 'fa-solid fa-bed'},
                {'url': 'card_manager', 'name': ' 卡片管理', 'icon': 'fa-solid fa-credit-card-alt'},
                {'url': 'notify_manager', 'name': ' 通知管理', 'icon': 'fa-solid fa-volume-high'},
            ]
        },
        {
            'name': '訂單管理功能',
            'id': 'mealsFunctionsMenu',
            'permission': ['caregiver'],
            'icon': 'fa-solid fa-utensils',
            'mode': 'multi',
            'items': [
                {'url': 'order_delivery_management', 'name': '餐點配送管理', 'icon': 'fa-truck'},
                {'url': 'main_course', 'name': '餐點管理', 'icon': 'fa-burger'},
                {'url': 'bom_settings', 'name': '餐點食材管理', 'icon': 'fa-solid fa-egg'},

            ]
        },
        {
            'name': '進銷存管理功能',
            'id': 'stockFunctionsMenu',
            'permission': ['caregiver'],
            'icon': 'fa-solid fa-truck-moving',
            'mode': 'multi',
            'items': [
                {'url': 'inventory_management', 'name': '食材庫存管理', 'icon': 'fa-solid fa-box-open'},
                {'url': 'purchase_detail', 'name': '食材進貨管理', 'icon': 'fa-solid fa-cart-flatbed'},
                {'url': 'suppliers', 'name': '食材供應商管理', 'icon': 'fa-solid fa-city'},
            ]
        }
    ]
    return {'function_menu': function_menu}