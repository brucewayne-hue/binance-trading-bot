from __future__ import annotations

from typing import Any

from bot.client import get_binance_client
from bot.logging_config import logger
from bot.validators import validate_inputs


def execute_order(
    *,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict[str, Any]:
    """
    Single shared execution path used by CLI/UI/API.
    Returns a dict that matches the mock exchange response.
    """

    symbol, side, order_type, quantity, price = validate_inputs(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    params: dict[str, str] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": str(quantity),
    }
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Limit parameters incomplete: Missing execution price floor target.")
        params["price"] = str(price)
        params["timeInForce"] = "GTC"

    logger.info(
        "ORDER -> Asset: %s | Side: %s | Type: %s | Qty: %s | Price: %s",
        symbol,
        side,
        order_type,
        quantity,
        price,
    )

    client = get_binance_client()
    return client.send_futures_order(params)

