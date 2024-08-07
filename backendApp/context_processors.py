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
            'url': 'medicine_order_management_review',
            'icon': 'fa-user-nurse'
        },
        {
            'name': '基本功能',
            'id': 'basicFunctionsMenu',
            'permission': ['caregiver'],
            'icon': 'fa-solid fa-ticket',
            'mode': 'multi',
            'items': [
                {'url': 'patient_manager', 'name': '被照護者管理', 'icon': 'fa-solid fa-hospital-user'},
                {'url': 'card_manager', 'name': ' 卡片管理', 'icon': 'fa-solid fa-credit-card-alt'},
                {'url': 'notify_manager', 'name': ' 通知管理', 'icon': 'fa-solid fa-volume-high'},
            ]
        },        
        {
            'name': '運輸機器人功能',
            'id': 'robotFunctionsMenu',
            'permission': ['caregiver'],
            'icon': 'fa-solid fa-vr-cardboard',
            'mode': 'multi',
            'items': [
                {'url': 'robot_manager', 'name': '機器人管理', 'icon': 'fa-solid fa-robot'},
                {'url': 'stop_point', 'name': ' 運送點管理', 'icon': 'fa-solid fa-briefcase'},
                {'url': 'turn_point_manager', 'name': ' 轉彎點管理', 'icon': 'fa-solid fa-magnet'}
            ]
        },
        {
            'name': '訂單管理功能',
            'id': 'mealsFunctionsMenu',
            'permission': ['caregiver'],
            'icon': 'fa-solid fa-utensils',
            'mode': 'multi',
            'items': [
                {'url': 'order_delivery_management', 'name': '餐點配送管理', 'icon': 'fa-solid fa-truck'},
                {'url': 'main_course', 'name': '餐點管理', 'icon': 'fa-solid fa-burger'},
                {'url': 'bom_settings', 'name': '餐點食材管理', 'icon': 'fa-solid fa-egg'},
                {'url': 'timeslot_manager', 'name': '用餐時段管理', 'icon': 'fa-solid fa-clock'},

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
        },
        {
            'name': '藥品管理',
            'id': 'medicineFunctionsMenu',
            'permission': ['pharmacy'],
            'icon': 'fa-solid fa-tablets',
            'mode': 'multi',
            'items': [
                {'url': 'medicine_order_management_review', 'name': '臨時用藥審核', 'icon': 'fa-solid fa-square-check'},
                {'url': 'medicine_order_management_delivery', 'name': '臨時用藥配送', 'icon': 'fa-solid fa-stethoscope'},
            ]
        }
    ]
    return {'function_menu': function_menu}