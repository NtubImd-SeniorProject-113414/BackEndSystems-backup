from backendApp.models import CourseSides, PurchaseDetail


def getSideStockBySidesId(sides_id):
    PurchaseQuantity = PurchaseDetail.calculateTotalQuantityBySideId(sides_id) #進貨總量
    OrderQuantity = CourseSides.calculateTotalQuantityBySideId(sides_id) #銷售總量
    return PurchaseQuantity - OrderQuantity
