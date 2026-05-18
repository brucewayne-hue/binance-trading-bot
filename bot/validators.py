from bot.logging_config import logger

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    if not symbol.endswith("USDT"):
        raise ValueError("Asset boundary mismatch: System mandates USDT-M pairs (e.g., BTCUSDT).")

    if side not in ["BUY", "SELL"]:
        raise ValueError("Invalid trade side setup. Use BUY or SELL.")

    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Unsupported execution profile. Options limited to MARKET or LIMIT.")

    if quantity <= 0:
        raise ValueError("Target volume criteria breach: Quantity must be greater than zero.")

    if order_type == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Limit parameters incomplete: Missing execution price floor target.")

    return symbol, side, order_type, quantity, price