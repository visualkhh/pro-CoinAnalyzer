#-*- coding: utf-8 -*-
import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import logging
from decimal import Decimal
import pprint
import configparser
import sys
from coinOne import CoinOne
logger = logging.getLogger("coinAnalyzer")
class CoinOneLimitBuy(CoinOne):

	PAYLOAD			= None
	"""
		PAYLOAD = {
		  "access_token": ACCESS_TOKEN,
		  "price": 500000,
		  "qty": 0.1,
		  "currency", "btc"
		}
	"""
	def __init__(self, config, payload):
		super().__init__('https://api.coinone.co.kr/v2/order/limit_buy/',config)
		self.PAYLOAD = payload


	def getPayLoad(self):
		logger.debug('name:{} url:{}   paylad:{}'.format(type(self).__name__, self.URL, self.PAYLOAD))
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
		"price": int(Decimal("4886500") + Decimal("-1000000")),
		"qty": 0.0001,
		"currency": "btc"
	}
	pprint.pprint(CoinOneLimitBuy(config, payload).get_result());