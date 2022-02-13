import os
import sys
import json
import requests
import time
import signing


class BitmexAPI(object):

    def __init__(self, config:dict):
        self.config = config
        self.apikey = str(config["BITMEX"]["APIKEY"])
        self.apisecret = str(config["BITMEX"]["APISECRET"])
        self.quoteurl = str(config["BITMEX"]["URLTEMPLATES"]["QUOTE"])
        self.limitorderurl = str(config["BITMEX"]["URLTEMPLATES"]["LIMITORDER"])
        self.limitorderpath = str(config["BITMEX"]["URLTEMPLATES"]["LIMITORDERPATH"])

    def PlaceLimitOrder(self, symbol, qty, price, orderType = "Buy"):
        payload = {}
        headers = {}

        payload["symbol"] = symbol
        payload["side"] = orderType
        payload["orderQty"] = qty
        payload["price"] = price
        payload["ordType"] = "Limit"
        payload = json.dumps(payload)

        print("Buy Limit Payload : " + str(payload))

        nonce = str(int(time.time()))
        signature = signing.bitmex_signature(self.apisecret,"POST",self.limitorderpath,nonce,payload)

        print("Buy Limit Order SIG : " + signature)


        headers["api-nonce"] = nonce
        headers["api-key"] = self.apikey
        headers["api-signature"] = signature

        res = requests.post(self.limitorderurl,data=payload, headers=headers)
        rbody = res.request.body
        rhead = res.request.headers
        res = res.json()

        print(res)
        return res

    def PlaceBuyLimitOrder(self, symbol,qty,price):
        return self.PlaceLimitOrder(symbol=symbol,qty=qty,price=price,orderType="Buy")

    def PlaceSellLimitOrder(self,symbol,qty,price):
        return self.PlaceLimitOrder(symbol=symbol, qty=qty, price=price, orderType="Sell")

    def __str__(self):
        res = str(self.quoteurl)
        return res
