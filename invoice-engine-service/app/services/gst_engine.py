from decimal import Decimal

def round_amount(value: Decimal) -> Decimal:
    """Round to 2 decimal places using standard rounding."""
    return value.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")

def calculate_line_item(
        unit_price: Decimal,
        quantity: Decimal,
        gst_rate: Decimal,
        is_interstate: bool = False
) -> dict:
    """ Calculate all amounts for one invoice line item.
        is_interstate = True  → IGST applies (selling across states)
        is_interstate = False → CGST + SGST applies (selling within same state)"""
    
    taxable_amount = round_amount(unit_price * quantity)      #Base amount before tax

    if is_interstate:                                           #Calculate tax based on transaction type
        igst_rate = gst_rate
        igst_amount = round_amount(taxable_amount * igst_rate / Decimal(100))
        cgst_rate = Decimal(0)
        sgst_rate = Decimal(0)
        cgst_amount = Decimal(0)
        sgst_amount = Decimal(0)
    else:
        cgst_rate = round_amount(gst_rate / 2)
        sgst_rate = round_amount(gst_rate / 2)
        cgst_amount = round_amount(taxable_amount * cgst_rate / Decimal(100))
        sgst_amount = round_amount(taxable_amount * sgst_rate / Decimal(100))
        igst_rate = Decimal(0)
        igst_amount = Decimal(0)

    #total

    total_amount = round_amount(taxable_amount + cgst_amount + sgst_amount + igst_amount)

    return {
        "taxable_amount": taxable_amount,
        "cgst_rate": cgst_rate,
        "sgst_rate": sgst_rate,
        "igst_rate": igst_rate,
        "cgst_amount": cgst_amount,
        "sgst_amount": sgst_amount,
        "igst_amount": igst_amount,
        "total_amount": total_amount
    }