import sys
import argparse
import bot.validators as validators
from bot.logging_config import logger
from bot.service import execute_order

def print_success_card(order_data):
    """Prints a highly visible, beautifully formatted trade execution card."""
    print("\n" + "=" * 50)
    print("STATUS SUCCESS: Testnet Trade Verified & Dispatched")
    print("=" * 50)
    print(f"Target Configuration: {order_data.get('symbol')} {order_data.get('side')} {order_data.get('type')}")
    print(f"Assigned Order ID:    {order_data.get('orderId')}")
    print(f"Current State Status: {order_data.get('status')}")
    print(f"Executed Volume Size: {order_data.get('executedQty')}")
    print(f"Average Entry Point:  {order_data.get('avgPrice')}")
    print("=" * 50 + "\n")

def run_interactive_wizard():
    """Launches an enhanced user terminal menu wizard to pick parameters cleanly."""
    print("\n" + "═" * 40)
    print("      ⚡ BINANCE TRADING BOT WIZARD ⚡      ")
    print("═" * 40)
    
    # 1. Choose Asset Symbol
    print("\n[1] Select Asset Token Symbol:")
    symbol = input("Enter symbol (Default: BTCUSDT): ").strip().upper() or "BTCUSDT"
    
    # 2. Choose Side
    print("\n[2] Select Order Execution Side:")
    print(" -> B : BUY")
    print(" -> S : SELL")
    side_input = input("Choose action side: ").strip().upper()
    side = "BUY" if side_input in ["B", "BUY"] else "SELL"
    
    # 3. Choose Order Type
    print("\n[3] Select Execution Profile Strategy Type:")
    print(" -> M : MARKET (Instant Liquidity)")
    print(" -> L : LIMIT (Boundary Constrained Price)")
    type_input = input("Choose execution type: ").strip().upper()
    order_type = "LIMIT" if type_input in ["L", "LIMIT"] else "MARKET"
    
    # 4. Choose Quantity
    print("\n[4] Define Transaction Size Volume Asset Weight:")
    quantity_input = input("Enter quantity scale (Default: 0.01): ").strip()
    quantity = float(quantity_input) if quantity_input else 0.01
    
    # 5. Choose Price (Only if Limit Order)
    price = None
    if order_type == "LIMIT":
        print("\n[5] Target Boundary Price Floor Trigger:")
        price_input = input("Enter target limit asset valuation price: ").strip()
        price = float(price_input) if price_input else 75000.0

    # Bundle params together
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }
    if price is not None:
        params["price"] = price
        
    return params

def main():
    parser = argparse.ArgumentParser(description="Algorithmic Testnet Order Routing Execution Gateway CLI.")
    parser.add_init = False
    parser.add_argument("--symbol", type=str, help="Target asset financial pairing trading ticker code.")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], help="Directional alignment profile vector.")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], help="Liquidity filling model configuration profile.")
    parser.add_argument("--quantity", type=float, help="Transaction target token unit volume size.")
    parser.add_argument("--price", type=float, help="Constraint floor trigger asset value price metric.")
    
    # Check if user didn't supply command arguments; if empty, trigger the bonus wizard!
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        # No arguments supplied -> Trigger the Interactive Menu Wizard Bonus feature!
        params = run_interactive_wizard()
    else:
        # Standard fallback processing for raw inline CLI commands
        params = {
            "symbol": args.symbol,
            "side": args.side,
            "type": args.type,
            "quantity": args.quantity
        }
        if args.price is not None:
            params["price"] = args.price

    # Core Execution Engine Workflow pipeline mapping
    try:
        logger.info(f"OUTBOUND REQUEST -> Asset: {params.get('symbol')} | Side: {params.get('side')} | Type: {params.get('type')} | Qty: {params.get('quantity')} | Price: {params.get('price')}")
        
        # Enforce validation schemas
        validators.validate_order_params(params)
        
        response = execute_order(
            symbol=params.get("symbol"),
            side=params.get("side"),
            order_type=params.get("type"),
            quantity=params.get("quantity"),
            price=params.get("price"),
        )
        
        if "orderId" in response:
            logger.info(f"INBOUND COMPLIANCE MATCH -> OrderID: {response['orderId']} | Status: {response['status']}")
            print_success_card(response)
        else:
            logger.error(f"BINANCE API ERROR: {response.get('msg')} (Code: {response.get('code')})")
            print(f"\n[EXCHANGE REJECTION] Binance rejected the order: {response.get('msg')}\n")
            
    except Exception as e:
        logger.error(f"RUNTIME EXECUTION CRITICAL HALT: {str(e)}")
        print(f"\n[SYSTEM FAILURE ERROR]: {str(e)}\n")

if __name__ == "__main__":
    main()