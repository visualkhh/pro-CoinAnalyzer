#-*- coding: utf-8 -*-
import websocket
import _thread
from threading import Thread, current_thread
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
#WAIT
BUY_WAIT_SEC 		= None
SELL_WAIT_SEC 		= None
#config end


# START_COIN 			= None	#Decimal(0) 			#시작금액
# DEST_COIN 			= None	#Decimal(0) 			#목적금액
START_KRW_QUOTE 	= None
START_BTC_BALANCE 	= None

KRW_QUOTE 			= None
BTC_BALANCE 		= None

BUY_WAIT			= False
SELL_WAIT			= False







def on_message(ws, message):
	# print("==========")
	try:
		global START_KRW_QUOTE, START_BTC_BALANCE, KRW_QUOTE, BTC_BALANCE, SELL_WAIT, BUY_WAIT

		krwQuote 		= Decimal(json.loads(message)['coinoneP'])						#1코인당 KRW
		krwBalance 		= Decimal(CoinOneBlance(CONFIG).get_result()['krw']['balance'])
		krwAvailBalance = Decimal(CoinOneBlance(CONFIG).get_result()['krw']['avail'])
		btcBalance 		= Decimal(CoinOneBlance(CONFIG).get_result()['btc']['balance'])
		btcAvailBalance = Decimal(CoinOneBlance(CONFIG).get_result()['btc']['avail'])

		#btc 잔액이 변경 되면 다시 시작한다.
		# if START_BTC_BALANCE and btcBalance > START_BTC_BALANCE:
		if START_BTC_BALANCE and BTC_BALANCE and START_BTC_BALANCE != BTC_BALANCE:
			START_KRW_QUOTE 	= None
			START_BTC_BALANCE 	= None

		if not START_KRW_QUOTE:
			START_KRW_QUOTE = krwQuote
		if not START_BTC_BALANCE:
			START_BTC_BALANCE = btcBalance


		if krwQuote!=KRW_QUOTE:
			logger.debug("*** KRW Quote Modify \t start({}) -> this({}) = |{}| ***".format(START_KRW_QUOTE, krwQuote, krwQuote-START_KRW_QUOTE))
		if btcBalance!=BTC_BALANCE:
			logger.debug("*** btc balance Modify \t start({}) -> availb({}) banlance({}) = |{}| ***".format(START_BTC_BALANCE, btcAvailBalance, btcBalance, btcBalance-START_BTC_BALANCE))
		KRW_QUOTE 	= krwQuote
		BTC_BALANCE = btcBalance

		startKRW 			= Decimal(START_KRW_QUOTE * btcBalance)							#시작금액
		sellKRW				= Decimal(startKRW + (startKRW * SELL_PER))						#판매 목적금액
		buyKRW				= Decimal(startKRW - (startKRW * BUY_PER))						#구매 목적금액
		sellQuotKRW			= Decimal(START_KRW_QUOTE + (START_KRW_QUOTE * SELL_PER))		#1btc당 krw 판매 목적금액
		buyQuotKRW			= Decimal(START_KRW_QUOTE - (START_KRW_QUOTE * BUY_PER))		#1btc당 krw 구매 목적금액

		startSellQuotePer 	= Decimal((krwQuote / sellQuotKRW) *100)		#1btc당 krw 판매 목표금액 100%달성하기위한 현재 상태
		startSellQuoteVal	= Decimal(sellQuotKRW - krwQuote)			#1btc당 krw 판매 목표금액 달성하기 위한 현재 부족한 금액상태
		thisKRW 			= Decimal(KRW_QUOTE * btcBalance)					#현재금액
		stateSellPer 		= Decimal((thisKRW / sellKRW) * 100)				#판매 목표금액 100%달성하기위한 현재 상태
		stateSellVal 		= Decimal(sellKRW - thisKRW)						#판매 목표금액 달성하기 위한 현재 부족한 금액상태


		startBuyQuotePer 	= Decimal((buyQuotKRW / krwQuote) *100)		#1btc당 krw 판매 목표금액 100%달성하기위한 현재 상태
		startBuyQuoteVal	= Decimal(krwQuote - buyQuotKRW)				#1btc당 krw 판매 목표금액 달성하기 위한 현재 부족한 금액상태
		stateBuyPer 		= Decimal(((buyKRW / thisKRW) * 100))				#구매 목표금액 100%달성하기위한 현재 상태
		stateBuyVal 		= Decimal(thisKRW - buyKRW)							#구매 목표금액 달성하기 위한 현재 부족한 금액상태

		stateStartThisVal 		= Decimal(thisKRW - startKRW)						#시작 금액에서 얼마만큼 상하인지
		stateStartThisQuoteVal 	= Decimal(krwQuote - START_KRW_QUOTE)				#1btc당 krw 시작 금액에서 얼마만큼 상하인지


		logger.debug("--SELL_WAIT:{} BUY_WAIT:{},  BTC:1btcKRWval({:10.8})  MY:btcBal({:10.8}  btcVal({:10.8})"
					 .format(SELL_WAIT,BUY_WAIT,krwQuote,btcBalance,thisKRW));

		# logger.debug("SELL STATE: S({:10.8}) \t W({:10.8}%, {:10.8}) \t -> \t E({:10.8}) = UD({:10.8})"
		# 	.format(startKRW, stateSellPer, stateSellVal, sellKRW, stateStartThisVal))
		logger.debug("SELL STATE: S({:10.8}) \t W({:10.8}%, {:10.8}) \t -> \t E({:10.8}) = UD({:10.8})"
			.format(START_KRW_QUOTE, startSellQuotePer, startSellQuoteVal, sellQuotKRW, stateStartThisQuoteVal))

		# logger.debug(" BUY STATE: S({:10.8}) \t W({:10.8}%, {:10.8}) \t -> \t E({:10.8}) = UD({:10.8})"
		# 	.format(startKRW, stateBuyPer, stateBuyVal, buyKRW, stateStartThisVal))
		logger.debug(" BUY STATE: S({:10.8}) \t W({:10.8}%, {:10.8}) \t -> \t E({:10.8}) = UD({:10.8})"
			.format(START_KRW_QUOTE, startBuyQuotePer, startBuyQuoteVal, buyQuotKRW, stateStartThisQuoteVal))




		#팔수있는 상황이면 팔아라
		if not SELL_WAIT and stateSellPer > Decimal(100):
			def run(*args):
				global SELL_WAIT
				SELL_WAIT = True
				logger.debug("thread start {} {}".format("sell", current_thread().getName()))
				try:
					result = sell(btcBalance, krwQuote)
					if result and '0'==result['errorCode']:
						time.sleep(SELL_WAIT_SEC)
				except Exception as e:
					logger.debug(e)
				finally:
					cancelSell()# time.sleep(1)
					SELL_WAIT = False
					logger.debug("thread end {} {}".format("sell", current_thread().getName()))
			Thread(target=run).start()


		# 살수 있는 상황이면 사라
		if not BUY_WAIT and stateBuyPer > Decimal(100):
			def run(*args):
				global BUY_WAIT
				BUY_WAIT = True
				logger.debug("thread start {} {}".format("buy", current_thread().getName()))
				try:
					result = buy(krwBalance, krwQuote)
					if result and '0'==result['errorCode']:
						time.sleep(BUY_WAIT_SEC)
				except Exception as e:
					logger.debug(e)
				finally:
					cancelBuy()
					BUY_WAIT = False
					logger.debug("thread end {} {}".format("buy", current_thread().getName()))
			Thread(target=run,).start()


	except Exception as e:
		logger.debug(e)


#매도
def sell(btcBalance, krwQuote):
	logger.debug("==sell==")
	if(btcBalance<Decimal("0.01")):
		logging.debug("Sell no request  low qty {} ".format(qty))
	payload = {
	  "price": int(krwQuote + KRW_SELL),
	  "qty": float(math.trunc(btcBalance*10000)/10000), #coinone은 소수점 4자리수까지만 받는다  최소단위 btc
	  "currency": "btc"
	}
	# log(sellPayload)
	result = CoinOneLimitSell(CONFIG, payload).get_result()
	logger.debug(result)
	return result
#매수
def buy(krwBalance, krwQuote):
	logger.debug("==buy==")
	qty = Decimal(krwBalance / krwQuote);
	if(qty<Decimal("0.01")):
		logging.debug("Buy no request  low qty {} ".format(qty))
		return
	payload = {
		"price": int(krwQuote + KRW_BUY),
		"qty": float(math.trunc(qty*10000)/10000),  #coinone은 소수점 4자리수까지만 받는다  최소단위 btc
		"currency": "btc"
	}
	# log(buyPayload)
	result = CoinOneLimitBuy(CONFIG, payload).get_result()
	logger.debug(result)
	return result

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

def on_error(ws, error):
	logger.debug(error)

def on_close(ws):
	logger.debug("### closed ###")

def on_open(ws):
	ws.send("{event: 'join', channel: 'live'}")
	# def run(*args):
	# 	for i in range(1):
	# 		time.sleep(1)
	# 		# ws.send("Hello %d" % i)
	# 		ws.send("{event: 'join', channel: 'live'}")
	# 		# result = ws.recv();
	# 		# print(result)
	# 	time.sleep(1)
	# 	# ws.close()
	# 	log("thread terminating...")
	# _thread.start_new_thread(run, ())

# def log(str):
	# print(str)
	# logger.debug(str)

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
	# log("START_COIN : {}".format(START_COIN))
	# log("DEST_COIN : {}".format(DEST_COIN))
	logger.debug("SELL_PER : {}".format(SELL_PER))
	logger.debug("BUY_PER : {}".format(BUY_PER))
	logger.debug("KRW_SELL : {}".format(KRW_SELL))
	logger.debug("KRW_BUY : {}".format(KRW_BUY))
	logger.debug("BUY_WAIT_SEC : {}".format(BUY_WAIT_SEC))
	logger.debug("SELL_WAIT_SEC : {}".format(SELL_WAIT_SEC))

	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://ws.coinone.co.kr:20013/",
								on_message = on_message,
								on_error = on_error,
								on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()