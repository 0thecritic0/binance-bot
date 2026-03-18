import os
import argparse
from dotenv import load_dotenv
from bot.client import BinanceFuturesClient
from bot.orders import place_market_order, place_limit_order
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import logger


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument(
        "--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)"
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side (BUY/SELL)",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type",
    )
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument(
        "--price", type=float, help="Order price (required for LIMIT orders)"
    )

    args = parser.parse_args()

    try:
        # 1. Input Validation
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)

        # 2. Setup Client
        load_dotenv()
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")

        if not api_key or not api_secret:
            print("❌ Error: API_KEY and API_SECRET must be set in your .env file")
            return

        client = BinanceFuturesClient(api_key, api_secret)

        # 3. Output Order Summary
        print(f"\n--- Order Request Summary ---")
        print(f"Symbol:   {symbol}")
        print(f"Side:     {side}")
        print(f"Type:     {order_type}")
        print(f"Quantity: {quantity}")
        if order_type == "LIMIT":
            print(f"Price:    {price}")
        print("-----------------------------\n")

        logger.info(f"Initiating {order_type} {side} order for {quantity} {symbol}")

        # 4. Execution
        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        else:
            response = place_limit_order(client, symbol, side, quantity, price)

        # 5. Output Response
        print("✅ Order successfully placed!")
        print(f"Order ID:      {response.get('orderId')}")
        print(f"Status:        {response.get('status')}")
        print(f"Executed Qty:  {response.get('executedQty')}")

        avg_price = response.get("avgPrice")
        if avg_price and float(avg_price) > 0:
            print(f"Average Price: {avg_price}")

    except Exception as e:
        logger.error(f"Application Error: {str(e)}")
        print(f"\n❌ Failed to place order: {str(e)}")


if __name__ == "__main__":
    main()
