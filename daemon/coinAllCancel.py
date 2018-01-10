#-*- coding: utf-8 -*-
import websocket
import _thread
import time
import json
import logging
import logging.handlers
import sys
import configparser
import math
import pprint
from decimal import Decimal
from coinOneBlance import CoinOneBlance
from coinOneMyLimitOrder import CoinOneMyLimitOrder
from coinOneLimitSell import CoinOneLimitSell
from coinOneLimitBuy import CoinOneLimitBuy
from coinOneCancel import CoinOneCancel


# logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger("coinAnalyzer")
logger.setLevel(logging.DEBUG)
# fileHandler와 StreamHandler를 생성
# file max size를 10MB로 설정
file_max_bytes = 10 * 1024 * 1024
# fileHandler = logging.FileHandler(filename='./log/my.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler = logging.handlers.RotatingFileHandler('./log/my.log', maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()
# formmater 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)
# Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)


##config
CONFIG		= None
SELL_PER 	= None	#Decimal(0.03) 			#수익률 퍼센트 EARN_PER
BUY_PER 	= None	#Decimal(0.03) 			#매도 퍼센트
KRW_SELL 	= None	#Decimal(100000000) 	#팔때 KRW에 얼마더 추가할건지
KRW_BUY 	= None	#Decimal(200000000) 	#살때 KRW에 얼마더 추가할건지
#config end


# START_COIN 			= None	#Decimal(0) 			#시작금액
# DEST_COIN 			= None	#Decimal(0) 			#목적금액
START_KRW_QUOTE 	= None
START_BTC_BALANCE 	= None

KRW_QUOTE 			= None


#WAIT
BUY_WAIT_SEC 		= None
SELL_WAIT_SEC 		= None





def cancel(atOrder):
	payload = {
		"order_id": atOrder['orderId'],
		"price": atOrder['price'],
		"qty": atOrder['qty'],
		"is_ask": 1 if 'ask'==atOrder['type'] else 0,
		"currency": "btc"
	}
	logger.debug(CoinOneCancel(CONFIG, payload).get_result())
	pass
def limitOrder():
	limitOrderPayload = {
		"currency": "btc"
	}
	limitOrder = CoinOneMyLimitOrder(CONFIG, limitOrderPayload).get_result();
	logger.debug(limitOrder)
	return limitOrder

#ask
def cancelSell():
	logger.debug("==cancelSell==")
	orders = limitOrder()
	for it in orders['limitOrders']:
		if('ask'==it['type']):
			cancel(it)

#bid
def cancelBuy():
	logger.debug("==cancelBuy==")
	orders = limitOrder()
	for it in orders['limitOrders']:
		if('bid'==it['type']):
			cancel(it)


# def logger.debug(str):
# 	print(str)
# 	logging.debug(str)

if __name__ == "__main__":
	config = configparser.ConfigParser()
	config.sections()
	configFile = sys.argv[1]
	configSection = sys.argv[2] if len(sys.argv)>=3 else "DEFAULT"
	config.read(configFile)
	config.sections()

	""" config setting
	[DEFAULT]
	ACCESS_TOKEN = eee
	SECRET_KEY = eee
	START_COIN = 0
	DEST_COIN = 0
	SELL_PER = 0.03
	BUY_PER = 0.03
	KRW_SELL = 100000000
	KRW_BUY = 200000000
	"""

	CONFIG 			= config[configSection]
	# START_COIN 	= Decimal(CONFIG['START_COIN'])
	# DEST_COIN 	= Decimal(CONFIG['DEST_COIN'])
	SELL_PER 		= Decimal(CONFIG['SELL_PER'])
	BUY_PER 		= Decimal(CONFIG['BUY_PER'])
	KRW_SELL 		= Decimal(CONFIG['KRW_SELL'])
	KRW_BUY 		= Decimal(CONFIG['KRW_BUY'])
	BUY_WAIT_SEC 	= Decimal(CONFIG['BUY_WAIT_SEC'])
	SELL_WAIT_SEC 	= Decimal(CONFIG['SELL_WAIT_SEC'])

	logger.debug("=====config=====")
	# logger.debug("START_COIN : {}".format(START_COIN))
	# logger.debug("DEST_COIN : {}".format(DEST_COIN))
	logger.debug("SELL_PER : {}".format(SELL_PER))
	logger.debug("BUY_PER : {}".format(BUY_PER))
	logger.debug("KRW_SELL : {}".format(KRW_SELL))
	logger.debug("KRW_BUY : {}".format(KRW_BUY))
	logger.debug("BUY_WAIT_SEC : {}".format(BUY_WAIT_SEC))
	logger.debug("SELL_WAIT_SEC : {}".format(SELL_WAIT_SEC))


	cancelSell()
	cancelBuy()