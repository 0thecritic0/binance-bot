from .client import BinanceFuturesClient


def place_market_order(
    client: BinanceFuturesClient, symbol: str, side: str, quantity: float
):
    params = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": quantity}
    return client.place_order(params)


def place_limit_order(
    client: BinanceFuturesClient, symbol: str, side: str, quantity: float, price: float
):
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC",  # Good Till Canceled is strictly required for limit orders
    }
    return client.place_order(params)
