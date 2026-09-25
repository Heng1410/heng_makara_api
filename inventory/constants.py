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