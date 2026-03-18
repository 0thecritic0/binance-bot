import time
import hmac
import hashlib
import requests
from typing import Dict, Any
from .logging_config import logger


class BinanceFuturesClient:
    # Set to the required testnet URL
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: Dict[str, Any]) -> str:
        """Generates the HMAC SHA256 signature required by Binance."""
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def place_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sends the signed order request to the testnet."""
        endpoint = "/fapi/v1/order"
        url = self.BASE_URL + endpoint

        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self._sign(params)

        logger.debug(f"Sending POST request to {url} with params: {params}")

        try:
            response = self.session.post(url, params=params)
            response_data = response.json()

            if response.status_code == 200:
                logger.info("API Request Successful.")
                logger.debug(f"API Response: {response_data}")
                return response_data
            else:
                logger.error(f"API Error ({response.status_code}): {response_data}")
                raise Exception(
                    f"Binance API Error: {response_data.get('msg', 'Unknown Error')}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {e}")
            raise Exception("Network error while contacting Binance API.")
