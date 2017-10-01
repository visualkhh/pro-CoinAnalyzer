#-*- coding: utf-8 -*-
import websocket
import _thread
import time
import json
import logging
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
logging.basicConfig(filename='log.log',format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

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






def on_message(ws, message):
	# print("==========")
	try:
		global START_KRW_QUOTE, START_BTC_BALANCE, KRW_QUOTE, startKRW, sellKRW

		krwQuote = Decimal(json.loads(message)['coinoneP'])						#1코인당 KRW
		krwBalance = Decimal(CoinOneBlance(CONFIG).get_result()['krw']['avail'])
		btcBalance = Decimal(CoinOneBlance(CONFIG).get_result()['btc']['avail'])

		#잔액이 상승되면 다시 시작한다.
		if START_BTC_BALANCE and btcBalance > START_BTC_BALANCE:
			START_KRW_QUOTE 	= None
			START_BTC_BALANCE 	= None

		if not START_KRW_QUOTE:
			START_KRW_QUOTE = krwQuote
		if not START_BTC_BALANCE:
			START_BTC_BALANCE = btcBalance


		if krwQuote!=KRW_QUOTE:
			log("*** KRW Quote Modify \t start({}) -> this({}) = |{}| ***".format(START_KRW_QUOTE, krwQuote, krwQuote-START_KRW_QUOTE))
		KRW_QUOTE = krwQuote

		startKRW 			= Decimal(START_KRW_QUOTE * btcBalance)				#시작금액
		sellKRW				= Decimal(startKRW + (startKRW * SELL_PER))			#판매 목적금액
		buyKRW				= Decimal(startKRW - (startKRW * BUY_PER))			#구매 목적금액

		thisKRW 			= Decimal(KRW_QUOTE * btcBalance)					#현재금액
		stateSellPer 		= Decimal((thisKRW / sellKRW) * 100)				#판매 목표금액 100%달성하기위한 현재 상태
		stateSellVal 		= Decimal(sellKRW - thisKRW)						#판매 목표금액 달성하기 위한 현재 부족한 금액상태

		stateBuyPer 		= Decimal(((buyKRW / thisKRW ) * 100))				#구매 목표금액 100%달성하기위한 현재 상태
		stateBuyVal 		= Decimal(thisKRW - buyKRW)							#구매 목표금액 달성하기 위한 현재 부족한 금액상태

		stateStartThisVal 	= Decimal(thisKRW - startKRW)						#시작 금액에서 얼마만큼 상하인지


		# log("SELL STATE: KRW // S({:}) C({:}) \t W({:}%, {:}) \t -> \t E({:}) = G{:}"
		# 	.format(startKRW, thisKRW, stateSellPer, stateSellVal, sellKRW, stateStartThisVal))
		log("SELL STATE: KRW // 1btc({:10.8}) S({:10.8}) C({:10.8}) \t W({:10.8}%, {:10.8}) \t -> \t E({:10.8}) = UD({:10.8})"
			.format(krwQuote, startKRW, thisKRW, stateSellPer, stateSellVal, sellKRW, stateStartThisVal))
		log(" BUY STATE: KRW // 1btc({:10.8}) S({:10.8}) C({:10.8}) \t W({:10.8}%, {:10.8}) \t -> \t E({:10.8}) = UD({:10.8})"
			.format(krwQuote, startKRW, thisKRW, stateBuyPer, stateBuyVal, buyKRW, stateStartThisVal))


		# time.sleep(10)

		#팔수있는 상황이면 팔아라
		if stateSellPer > Decimal(100):
			cancelSell()
			time.sleep(1)
			result = sell(btcBalance, krwQuote)
			if '0'==result['errorCode']:
				time.sleep(SELL_WAIT_SEC)
		# 살수 있는 상황이면 사라
		if stateBuyPer > Decimal(100):
			cancelBuy()
			time.sleep(1)
			result = buy(krwBalance, krwQuote)
			if '0'==result['errorCode']:
				time.sleep(BUY_WAIT_SEC)
	except Exception as e:
		log(e)


#매도
def sell(btcBalance, krwQuote):
	log("==sell==")
	payload = {
	  "price": int(krwQuote + KRW_SELL),
	  "qty": float(math.trunc(btcBalance*10000)/10000), #coinone은 소수점 4자리수까지만 받는다  최소단위 btc
	  "currency": "btc"
	}
	# log(sellPayload)
	result = CoinOneLimitSell(CONFIG, payload).get_result()
	log(result)
	return result
#매수
def buy(krwBalance, krwQuote):
	log("==buy==")
	qty = krwBalance / krwQuote;
	payload = {
		"price": int(krwBalance + KRW_BUY),
		"qty": float(math.trunc(qty*10000)/10000),  #coinone은 소수점 4자리수까지만 받는다  최소단위 btc
		"currency": "btc"
	}
	# log(buyPayload)
	result = CoinOneLimitBuy(CONFIG, payload).get_result()
	log(result)
	return result

def cancel(atOrder):
	payload = {
		"order_id": atOrder['orderId'],
		"price": atOrder['price'],
		"qty": atOrder['qty'],
		"is_ask": 1 if 'ask'==atOrder['type'] else 0,
		"currency": "btc"
	}
	log(CoinOneCancel(CONFIG, payload).get_result())
	pass
def limitOrder():
	limitOrderPayload = {
		"currency": "btc"
	}
	limitOrder = CoinOneMyLimitOrder(CONFIG, limitOrderPayload).get_result();
	log(limitOrder)
	return limitOrder

#ask
def cancelSell():
	log("==cancelSell==")
	orders = limitOrder()
	for it in orders['limitOrders']:
		if('ask'==it['type']):
			cancel(it)

#bid
def cancelBuy():
	log("==cancelBuy==")
	orders = limitOrder()
	for it in orders['limitOrders']:
		if('bid'==it['type']):
			cancel(it)

def on_error(ws, error):
	log(error)

def on_close(ws):
	log("### closed ###")

def on_open(ws):
	def run(*args):
		for i in range(1):
			time.sleep(1)
			# ws.send("Hello %d" % i)
			ws.send("{event: 'join', channel: 'live'}")
			# result = ws.recv();
			# print(result)
		time.sleep(1)
		# ws.close()
		log("thread terminating...")
	_thread.start_new_thread(run, ())

def log(str):
	print(str)
	logging.debug(str)

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

	log("=====config=====")
	# log("START_COIN : {}".format(START_COIN))
	# log("DEST_COIN : {}".format(DEST_COIN))
	log("SELL_PER : {}".format(SELL_PER))
	log("BUY_PER : {}".format(BUY_PER))
	log("KRW_SELL : {}".format(KRW_SELL))
	log("KRW_BUY : {}".format(KRW_BUY))
	log("BUY_WAIT_SEC : {}".format(BUY_WAIT_SEC))
	log("SELL_WAIT_SEC : {}".format(SELL_WAIT_SEC))

	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://ws.coinone.co.kr:20013/",
								on_message = on_message,
								on_error = on_error,
								on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()