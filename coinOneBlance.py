#-*- coding: utf-8 -*-
import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import pprint
import logging
import configparser
import sys
from coinOne import CoinOne

logger = logging.getLogger("coinAnalyzer")
class CoinOneBlance(CoinOne):

	def __init__(self, config):
		super().__init__('https://api.coinone.co.kr/v2/account/balance/',config)

	def getPayLoad(self):
		payload = {}
		return payload;



if __name__   == "__main__":
	config = configparser.ConfigParser()
	config.sections()
	configFile = sys.argv[1]
	configSection = sys.argv[2] if len(sys.argv)>=3 else "DEFAULT"
	config.read(configFile)
	config.sections()
	config 		= config[configSection]

	pprint.pprint(CoinOneBlance(config).get_result());