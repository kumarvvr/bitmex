import os
import sys
import json
import time
from pathlib import Path
from BitmexWrapper import BitAPIWrapper


repeat_minutes = 1

curdir = Path.cwd()

# region External Files
config = None
configfile = curdir / "config.json"


# endregion

# region External File Access

# Load the config data...

with configfile.open() as cf:
    config = json.load(cf)

# endregion

apikey = config["BITMEX"]["APIKEY"]
apisec = config["BITMEX"]["APISECRET"]

repeat_minutes = int(config["REPEAT_EVERY_X_MINUTES"])

buypricefactor = float(config["BOT"]["BUYLIMITPERCENTAGE"])
buypricefactor = 1.0 - (buypricefactor/100.0)

sellpricefactor = float(config["BOT"]["SELLLIMITPERCENTAGE"])
sellpricefactor = 1.0 + (sellpricefactor/100.0)

quantity = int(config["BOT"]["QUANTITY"])

timedelay = int(config["BOT"]["DELAY_BETWEEN_ORDERS"])

currencylist = config["CURRENCY_LIST"]

failure_repeat_count = int(config["FAILURE_REPEAT_COUNT"])
failure_repeat_delay = int(config["FAILURE_REPEAT_DELAY"])


wrapper = BitAPIWrapper(api_key=apikey, api_secret=apisec,isDemo=False)

def PlaceOrders():
    global wrapper, currencylist, buypricefactor, sellpricefactor, quantity, timedelay

    for currency in currencylist:
        presentprice = wrapper.GetPrice(sym=currency)
        buyprice = int(presentprice*buypricefactor)
        sellprice = int(presentprice*sellpricefactor)
        print("--------------------------------------------")
        print("Current Price of "+currency+" is "+ str(presentprice))
        print("--------------------------------------------")
        try:
            res = wrapper.PlaceBuyLimitOrder(sym=currency, price=buyprice, qty=quantity)
        except Exception as e:
            print("Error executing above trade ####> " + str(e))
            print("Repeating until max count or success")
            count = 0
            completed = False
            while count <= failure_repeat_count:
                count+=1
                time.sleep(failure_repeat_delay)
                try:
                    res = wrapper.PlaceBuyLimitOrder(sym=currency, price=buyprice, qty=quantity)
                    completed = True
                    break
                except Exception as e:
                    print("Retrial : "+str(count))
            if not completed:
                print("Error completing last Buy Limit Order")
        time.sleep(timedelay)

        if completed:
            try:
                res = wrapper.PlaceSellLimitOrder(sym=currency, price=sellprice, qty=quantity)
            except Exception as e:
                print("Error executing above trade ####> " + str(e))
                print("Repeating until max count or success")
                count = 0
                completed = False

                while count <= failure_repeat_count:
                    count += 1
                    time.sleep(failure_repeat_delay)
                    try:
                        res = wrapper.PlaceSellLimitOrder(sym=currency, price=sellprice, qty=quantity)
                        completed = True
                        break
                    except Exception as e:
                        print("Retrial : " + str(count))
                if not completed:
                    print("Error completing last Sell Limit Order")
        else:
            print("Skipping a sell order as the buy order failed.")


def PrintOverWrite(message):
    sys.stdout.write(message+"                                           \r")
    sys.stdout.flush()

if __name__ == '__main__':

    while(True):
        PlaceOrders()
        rms = repeat_minutes*60
        while(rms > 0):
            PrintOverWrite("Trade will repeat in : "+str(rms)+" seconds")
            time.sleep(1)
            rms = rms-1




