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
from coinOne import  CoinOne


class CoinOneMyLimitOrder(CoinOne):
	"""
	PAYLOAD = {
		"access_token": ACCESS_TOKEN,
		"currency": "btc"
	}
	"""
	PAYLOAD			= None

	def __init__(self, config, payload):
		super().__init__('https://api.coinone.co.kr/v2/order/limit_orders/', config)
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
		"currency": "btc"
	}
	pprint.pprint(CoinOneMyLimitOrder(config, payload).get_result());