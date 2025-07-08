from binance.client import Client
from binance.enums import *
from loguru import logger

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        logger.add("bot.log", rotation="500 KB")
        logger.info("Bot initialized.")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                logger.error("Unsupported order type.")
                return None

            logger.success(f"Order placed: {order}")
            return order

        except Exception as e:
            logger.exception("Order placement failed.")
            return None


def main():
    api_key = input("Enter your Binance API Key: ")
    api_secret = input("Enter your Binance API Secret: ")

    bot = BasicBot(api_key, api_secret)

    symbol = input("Enter trading pair (e.g., BTCUSDT): ").upper()
    action = input("Order side (buy/sell): ").lower()
    side = SIDE_BUY if action == 'buy' else SIDE_SELL
    order_type = input("Order type (MARKET/LIMIT): ").upper()
    quantity = float(input("Enter quantity: "))

    price = None
    if order_type == 'LIMIT':
        price = float(input("Enter limit price: "))

    order = bot.place_order(symbol, side, order_type, quantity, price)
    if order:
        print("✅ Order placed successfully!")
    else:
        print("❌ Order failed. Check logs for details.")

if __name__ == "__main__":
    main()