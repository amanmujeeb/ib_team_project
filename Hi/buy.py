from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time
import pandas


#Qusestion 3

#Traded Price for AAPL
fir_contract = Contract()
fir_contract.symbol = 'AAPL'
fir_contract.secType = 'STK'
fir_contract.exchange = 'SMART'
fir_contract.currency = 'USD'

app = IBapi()
app.connect('127.0.0.1', 7497, 0)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)

#Request historical candles
app.reqHistoricalData(1, fir_contract, '', '1 D', '1 min', 'TRADES', 0, 2, False, [])
time.sleep(5) #sleep to allow enough time for data to be returned

df = pandas.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low','Volume'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
print('Retrieve minute-bar Traded Price for AAPL:')
print(df)
app.disconnect()

#BID Price for AAPL
app = IBapi()
app.connect('127.0.0.1', 7497, 0)
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)
app.reqHistoricalData(1, fir_contract, '', '1 D', '1 min', 'BID',0, 2, False, [])
time.sleep(5)
df = pandas.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low','Volume'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
print('Retrieve minute-bar BID prices for AAPL:')
print(df)
app.disconnect()


#ASK Price for AAPL
app = IBapi()
app.connect('127.0.0.1', 7497, 0)
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)
app.reqHistoricalData(1, fir_contract, '', '1 D', '1 min', 'ASK', 0, 2, False, [])
time.sleep(5)
df = pandas.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low','Volume'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
print('Retrieve minute-bar ASK prices for AAPL:')
print(df)
app.disconnect()





#Traded Price for AMZN

amz_contract = Contract()
amz_contract.symbol = 'AMZN'
amz_contract.secType = 'STK'
amz_contract.exchange = 'SMART'
amz_contract.currency = 'USD'

app = IBapi()
app.connect('127.0.0.1', 7497, 0)
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)
app.reqHistoricalData(1, amz_contract, '', '1 D', '1 min', 'TRADES', 0, 2, False, [])
time.sleep(5)
df = pandas.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low','Volume'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
print('Retrieve minute-bar Traded Price for AMZN:')
print(df)
app.disconnect()

#BID Price for AMZN
app = IBapi()
app.connect('127.0.0.1', 7497, 0)
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)
app.reqHistoricalData(1, amz_contract, '', '1 D', '1 min', 'BID', 0, 2, False, [])
time.sleep(5)
df = pandas.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low','Volume'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
print('Retrieve minute-bar BID Price for AMZN:')
print(df)
app.disconnect()

#ASK Price for AMZN
app = IBapi()
app.connect('127.0.0.1', 7497, 0)
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)
app.reqHistoricalData(1, amz_contract, '', '1 D', '1 min', 'ASK', 0, 2, False, [])
time.sleep(5)
df = pandas.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low','Volume'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
print('Retrieve minute-bar ASK Price for AMZN:')
print(df)
app.disconnect()





#Place "Market Order" to buy 100 shares of NFLX (Netflix).
class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId , errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId ):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract = Contract()
        contract.symbol = "NFLX"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        order = Order()
        order.action = "BUY"
        order.totalQuantity = 100
        order.orderType = "MKT"

        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    app = TestApp()
    app.nextOrderId = 0
    app.connect("127.0.0.1", 7497, 9)

    Timer(3, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()


#Place an "Market Order" to buy 100 shares of AAPL (Apple).

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId , errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId ):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        order = Order()
        order.action = "BUY"
        order.totalQuantity = 100
        order.orderType = "MKT"


        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    app = TestApp()
    app.nextOrderId = 0
    app.connect("127.0.0.1", 7497, 9)

    Timer(3, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()

#Place a "Limit Order" to buy 100 shares of GOOG and Cancel the open order

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)


def run_loop():
    app.run()


# Function to create FX Order contract
def FX_order(self):
    contract = Contract()
    contract.symbol = "GOOG"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


app = IBapi()
app.connect('127.0.0.1', 7497, 123)

app.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Check if the API is connected via orderid
while True:
    if isinstance(app.nextorderId, int):
        print('connected')
        break
    else:
        print('waiting for connection')
        time.sleep(1)

# Create order object
order = Order()
order.action = 'BUY'
order.totalQuantity = 100
order.orderType = 'LMT'
order.lmtPrice = '90'

# Place order
app.placeOrder(app.nextorderId, FX_order('EURUSD'), order)
# app.nextorderId += 1

time.sleep(3)

# Cancel order
print('cancelling order')
app.cancelOrder(app.nextorderId)

time.sleep(3)
app.disconnect()
