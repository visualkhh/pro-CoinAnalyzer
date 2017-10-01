#-*- coding: utf-8 -*-
import websocket
import _thread
import time
import json
import logging
import sys
import configparser
from decimal import Decimal
from coinOneBlance import CoinOneBlance
logging.basicConfig(filename='log.log',format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

##config
CONFIG		= None
START_COIN 	= None	#Decimal(0) 			#시작금액
DEST_COIN 	= None	#Decimal(0) 			#목적금액
SELL_PER 	= None	#Decimal(0.03) 			#수익률 퍼센트 EARN_PER
BUY_PER 	= None	#Decimal(0.03) 			#매도 퍼센트
KRW_SELL 	= None	#Decimal(100000000) 	#팔때 KRW에 얼마더 추가할건지
KRW_BUY 	= None	#Decimal(200000000) 	#살때 KRW에 얼마더 추가할건지
#config end

START_KRW_QUOTE 	= None
START_BTC_BALANCE 	= None


KRW_QUOTE 			= None
def on_message(ws, message):
	# print("==========")
	try:
		global START_KRW_QUOTE, START_BTC_BALANCE, KRW_QUOTE

		krwQuote = Decimal(json.loads(message)['coinoneP'])						#1코인당 KRW
		balance = Decimal(CoinOneBlance(CONFIG).get_result()['btc']['avail'])

		#잔액이 상승되면 다시 시작한다.
		if START_BTC_BALANCE and balance > START_BTC_BALANCE:
			START_KRW_QUOTE 	= None
			START_BTC_BALANCE 	= None

		if not START_KRW_QUOTE:
			START_KRW_QUOTE = krwQuote
		if not START_BTC_BALANCE:
			START_BTC_BALANCE = balance


		if krwQuote!=KRW_QUOTE:
			log("*** KRW Quote Modify \t start({}) -> this({}) = {} ***".format(START_KRW_QUOTE, krwQuote, krwQuote-START_KRW_QUOTE))
		KRW_QUOTE = krwQuote




		# START_COIN 		= Decimal(bal['btc']['avail'])						#시작금액
		# DEST_COIN		= Decimal(START_COIN + (START_COIN * EARN_PER))		#목적금액
		# stateDestPer 	= Decimal(START_COIN / DEST_COIN * 100)				#목표금액 100%달성하기위한 현재 상태
		# stateDestVal 	= Decimal(DEST_COIN - START_COIN)					#목표금액 달성하기 위한 현재 부족한 금액상태

		# start_krw 		= Decimal(krw * Decimal(bal['btc']['avail']))		#시작금액
		# dest_krw		= Decimal(start_krw + (start_krw * EARN_PER))		#목적금액
		# stateKrwDestPer = Decimal(start_krw / dest_krw * 100)				#목표금액 100%달성하기위한 현재 상태
		# stateKrwDestVal = Decimal(dest_krw - start_krw)						#목표금액 달성하기 위한 현재 부족한 금액상태

		# print ("BTC: {:10.8} \t ({:10.8}%, {:10.10}) \t -> \t {:10.8}".format(START_COIN, stateDestPer, stateDestVal, DEST_COIN))
		# print ("KRW: {:10.8} \t ({:10.8}%, {:10.10}) \t -> \t {:10.8}".format(start_krw, stateKrwDestPer, stateKrwDestVal, dest_krw))




		START_COIN 			= Decimal(START_KRW_QUOTE * balance)				#시작금액
		DEST_COIN			= Decimal(START_COIN + (START_COIN * SELL_PER))		#목적금액

		thisCoin 			= Decimal(KRW_QUOTE * balance)						#현재금액
		stateDestPer 		= Decimal(thisCoin / DEST_COIN * 100)				#목표금액 100%달성하기위한 현재 상태
		stateDestVal 		= Decimal(DEST_COIN - thisCoin)						#목표금액 달성하기 위한 현재 부족한 금액상태
		stateStartThisVal 	= Decimal(thisCoin - START_COIN)					#시작 금액에서 얼마만큼 상하인지


		log("BTC: {:10.8} \t ({:10.8}%, {:10.8}) \t -> \t {:10.8} = {:10.8}".format(START_COIN, stateDestPer, stateDestVal, DEST_COIN, stateStartThisVal))

	except Exception as e:
		log(e)


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

	CONFIG 		= config[configSection]
	START_COIN 	= Decimal(CONFIG['START_COIN'])
	DEST_COIN 	= Decimal(CONFIG['DEST_COIN'])
	SELL_PER 	= Decimal(CONFIG['SELL_PER'])
	BUY_PER 	= Decimal(CONFIG['BUY_PER'])
	KRW_SELL 	= Decimal(CONFIG['KRW_SELL'])
	KRW_BUY 	= Decimal(CONFIG['KRW_BUY'])


	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://ws.coinone.co.kr:20013/",
								on_message = on_message,
								on_error = on_error,
								on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()