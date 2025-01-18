import time
import requests
import hmac
import base64
import json
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()

class OKXClient:
    def __init__(self, api_key, api_secret, passphrase, is_test=False):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.PASSPHRASE = passphrase
        self.BASE_URL = 'https://www.okx.com'
        self.is_test = is_test

    def _create_signature(self, timestamp, method, request_path, body):
        message = f"{timestamp}{method}{request_path}{body}"
        mac = hmac.new(
            bytes(self.API_SECRET, encoding='utf-8'),
            bytes(message, encoding='utf-8'),
            digestmod='sha256'
        )
        return base64.b64encode(mac.digest()).decode()

    def _send_request(self, method, path, body=None):
        body = body or {}
        timestamp = datetime.utcnow().isoformat("T", "milliseconds") + "Z"
        body_str = json.dumps(body) if body else ""
        
        headers = {
            'OK-ACCESS-KEY': self.API_KEY,
            'OK-ACCESS-SIGN': self._create_signature(timestamp, method.upper(), path, body_str),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.PASSPHRASE,
            'Content-Type': 'application/json'
        }

        url = self.BASE_URL + path
        response = requests.request(method, url, headers=headers, data=body_str)
        return response.json()

    def get_funding_rate(self, inst_id):
        """获取资金费率"""
        try:
            response = self._send_request(
                "GET", 
                f"/api/v5/public/funding-rate?instId={inst_id}"
            )
            return float(response['data'][0]['fundingRate'])
        except Exception as e:
            logger.error(f"获取资金费率失败: {str(e)}")
            return None

    def get_ticker(self, inst_id):
        """获取最新价格"""
        try:
            response = self._send_request(
                "GET", 
                f"/api/v5/market/ticker?instId={inst_id}"
            )
            return float(response['data'][0]['last'])
        except Exception as e:
            logger.error(f"获取价格失败: {str(e)}")
            return None
