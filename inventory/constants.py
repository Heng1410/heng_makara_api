class StockMovementType:
    RESTOCK = "RESTOCK"
    SALE = "SALE"
    RETURN = "RETURN"
    ADJUSTMENT = "ADJUSTMENT"
    DAMAGE = "DAMAGE"
    EXPIRED = "EXPIRED"

    CHOICES = (
        (RESTOCK, "Restock"),
        (SALE, "Sale"),
        (RETURN, "Return"),
        (ADJUSTMENT, "Adjustment"),
        (DAMAGE, "Damage"),
        (EXPIRED, "Expired"),
    )

    REMOVAL_TYPES = (
        SALE,
        DAMAGE,
        EXPIRED,
        ADJUSTMENT,
    )

    STOCK_MOVEMENT_RESTOCK = "restock"
    STOCK_MOVEMENT_SALE = "sale"
    STOCK_MOVEMENT_ADJUSTMENT = "adjustment"

    STOCK_MOVEMENT_TYPES = (
        (STOCK_MOVEMENT_RESTOCK, "Restock"),
        (STOCK_MOVEMENT_SALE, "Sale"),
        (STOCK_MOVEMENT_ADJUSTMENT, "Adjustment"),
    )
