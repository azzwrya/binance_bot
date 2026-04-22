import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        # Initialize client and explicitly set to testnet
        self.client = Client(api_key, api_secret, testnet=True)
        # Force the base URL for the Futures Testnet API
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi/v1'

    def place_futures_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        try:
            params = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity,
            }
            
            if order_type.upper() == "LIMIT":
                if not price:
                    raise ValueError("Price is required for LIMIT orders.")
                params["price"] = str(price)
                params["timeInForce"] = "GTC"  # Good Till Cancelled

            logger.info(f"Sending Order Request: {params}")
            response = self.client.futures_create_order(**params)
            logger.info(f"Order Successful. Order ID: {response.get('orderId')}")
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message} (Code: {e.code})")
            raise
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            raise