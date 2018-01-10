# pro-CoinAnalyzer
pro-CoinAnalyzer
안녕하세요.  연휴동안 심심해서 만들어본

코인원 매도,매수 프로그램입니다.

주변에서 가상화폐 하시는분이 계셔서 한 100만원만 해볼까 해서 시작하다.

API문서 가 잘되어있길래 한번 만들어보았어요 ㅎ


기본적인 로직은

1. 투자금액(시작) 에서 특정 ?% 오르면  매도

2. 특정 ?% 내리면  매수

입니다. 별거없어요 ㅎ


-------
config.ini

[DEFAULT]

ACCESS_TOKEN = 7*******bb

SECRET_KEY = 7********bb

BUY_PER = 0.03

SELL_PER = 0.03

KRW_BUY = -5000

KRW_SELL = 5000

BUY_WAIT_SEC = 25

SELL_WAIT_SEC = 25

KRW_DEFEN = 1000000

BTC_DEFEN = 0.0001



#START_KRW_QUOTE = 5126000

#START_BTC_BALANCE = 0.2166830

INIT_KRW_BALANCE = 1000000
