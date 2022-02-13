import bitmex

class BitAPIWrapper(object):

    def __init__(self, api_key, api_secret, isDemo=True):
        self.key = api_key
        self.secret = api_secret
        self.bitmex = bitmex.bitmex(test=isDemo,api_key=self.key, api_secret=self.secret)

    def GetPrice(self, sym = ""):
        if (sym == ""):
            return None
        else:
            res = None
            res = self.bitmex.Quote.Quote_get(symbol=sym, reverse=True, count=1).result()
            price = res[0][0]['bidPrice']
            return price

    def PlaceBuyLimitOrder(self, sym, price, qty):
        print("\n")
        print("###############-------------###############")
        print("Buy Limit : "+ sym +" , at Price : "+str(price) +" , for Quantity : "+ str(qty))
        print("###############-------------###############")

        res = self.bitmex.Order.Order_new(symbol = sym,orderQty=qty,price=price, ordType="Limit").result()
        return res[0][0]

    def PlaceSellLimitOrder(self, sym, price, qty):
        qty = qty * -1
        print("\n")
        print("###############-------------###############")
        print("Buy Limit : " + sym + " , at Price : " + str(price) + " , for Quantity : " + str(qty))
        print("###############-------------###############")

        res = self.bitmex.Order.Order_new(symbol = sym,orderQty=qty,price=price, ordType="Limit").result()
        return res[0][0]
