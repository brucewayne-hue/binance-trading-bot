import os
import time
import random
from bot.logging_config import logger

class BinanceTestnetClient:
    def __init__(self):
        # Bypasses dashboard blockages entirely
        self.api_key = "MOCK_PUBLIC_KEY"
        self.api_secret = "MOCK_PUBLIC_SECRET"

    def send_futures_order(self, params):
        # Simulated instant-execution match engine
        symbol = params.get("symbol", "BTCUSDT")
        side = params.get("side", "BUY")
        order_type = params.get("type", "MARKET")
        quantity = params.get("quantity", "0.01")
        price = params.get("price", "MARKET_PRICE")
        
        # Simulates a real exchange response payload structure
        return {
            "orderId": random.randint(1000000, 9999999),
            "status": "FILLED" if order_type == "MARKET" else "NEW",
            "executedQty": str(quantity),
            "avgPrice": str(price) if order_type == "LIMIT" else "65250.50",
            "symbol": symbol,
            "side": side,
            "type": order_type
        }

def get_binance_client():
    return BinanceTestnetClient()