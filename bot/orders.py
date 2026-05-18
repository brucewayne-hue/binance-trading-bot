from bot.logging_config import logger
from bot.client import get_binance_client

def place_futures_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    try:
        client = get_binance_client()
        
        logger.info(f"OUTBOUND REQUEST -> Asset: {symbol} | Side: {side} | Type: {order_type} | Qty: {quantity} | Price: {price}")
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": str(quantity)
        }
        
        if order_type == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"

        # Direct REST call execution
        response = client.send_futures_order(params)
        
        # Catch exchange side credential or format blocks
        if "code" in response and "msg" in response:
            logger.error(f"BINANCE API ERROR: {response.get('msg')} (Code: {response.get('code')})")
            print(f"\n[EXCHANGE REJECTION] Binance rejected the order: {response.get('msg')}\n")
            return response

        logger.info(f"INBOUND COMPLIANCE MATCH -> OrderID: {response.get('orderId')} | Status: {response.get('status')}")
        
        print("\n" + "="*50)
        print("STATUS SUCCESS: Testnet Trade Verified & Dispatched")
        print("="*50)
        print(f"Target Configuration: {symbol} {side} {order_type}")
        print(f"Assigned Order ID:    {response.get('orderId')}")
        print(f"Current State Status: {response.get('status')}")
        print(f"Executed Volume Size: {response.get('executedQty')}")
        print(f"Average Entry Point:  {response.get('avgPrice', '0.0')}")
        print("="*50 + "\n")
        
        return response

    except Exception as runtime_ex:
        logger.error(f"NETWORK SYSTEM LEVEL EXCEPTION: {str(runtime_ex)}")
        print(f"\n[CORE CRITICAL ERROR] Platform engine halted: {str(runtime_ex)}\n")