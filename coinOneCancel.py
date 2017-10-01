#-*- coding: utf-8 -*-
import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import pprint
import configparser
import sys
from coinOne import CoinOne


class CoinOneCancel(CoinOne):
	PAYLOAD			= None
	"""
	PAYLOAD = {
		"access_token": ACCESS_TOKEN,
		"order_id": "OrderID",
		"price": 500000,
		"qty": 0.1,
		"is_ask": 1,
		"currency": "btc"
	}
	"""


	def __init__(self, config, payload):
		super().__init__('https://api.coinone.co.kr/v2/order/cancel/',config)
		self.PAYLOAD = payload



	def getPayLoad(self):
		self.log('name:{} url:{}   paylad:{}'.format(type(self).__name__, self.URL, self.PAYLOAD))
		return self.PAYLOAD


if __name__   == "__main__":
	config = configparser.ConfigParser()
	config.sections()
	configFile = sys.argv[1]
	configSection = sys.argv[2] if len(sys.argv)>=3 else "DEFAULT"
	config.read(configFile)
	config.sections()
	config 		= config[configSection]
	payload = {
		"order_id": "c68ca074-62c3-4fcb-955e-39e45f894781",
		"price": 3886500,
		"qty": 0.0001,
		"is_ask": 0,
		"currency": "btc"
	}
	pprint.pprint(CoinOneCancel(config,payload).get_result());