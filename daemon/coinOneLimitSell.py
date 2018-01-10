#-*- coding: utf-8 -*-
import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import pprint
import logging
from decimal import Decimal
import configparser
import sys
from coinOne import CoinOne
logger = logging.getLogger("coinAnalyzer")
class CoinOneLimitSell(CoinOne):

	PAYLOAD = None
	"""
	PAYLOAD = {
	  "access_token": ACCESS_TOKEN,
	  "price": 500000,
	  "qty": 0.1,
	  "currency": "btc"
	}
	"""

	def __init__(self, config, payload):
		super().__init__('https://api.coinone.co.kr/v2/order/limit_sell/',config)
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
 	#paylad:{'qty': 0.216483, 'currency': 'btc', 'price': 14894000}
	payload = {
	  	"price": int(Decimal("4886500") + Decimal("+1000000")), #시세값보다 비싸게
		"qty": 0.2164,
		"currency": "btc"
	}
	pprint.pprint(CoinOneLimitSell(config, payload).get_result());