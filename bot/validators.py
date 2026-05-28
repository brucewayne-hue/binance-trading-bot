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


def validate_order_params(params: dict):
    """
    Backwards-compatible validator used by `bot.cli`.
    Normalizes values and raises ValueError on invalid input.
    """

    symbol = params.get("symbol", "BTCUSDT")
    side = params.get("side", "BUY")
    order_type = params.get("type", "MARKET")
    quantity = params.get("quantity", 0.01)
    price = params.get("price", None)

    symbol, side, order_type, quantity, price = validate_inputs(
        symbol=str(symbol),
        side=str(side),
        order_type=str(order_type),
        quantity=float(quantity),
        price=float(price) if price is not None else None,
    )

    params["symbol"] = symbol
    params["side"] = side
    params["type"] = order_type
    params["quantity"] = quantity
    if price is not None:
        params["price"] = price

    return params