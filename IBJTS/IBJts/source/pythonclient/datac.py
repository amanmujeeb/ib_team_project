from ibapi.client import *
from ibapi.wrapper import *
import time
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import *
from threading import Timer
import pandas as pd

class GetHistorical(EWrapper, EClient):
    def _init_(self):
        EClient._init_(self, self)
        self.df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        self.df.loc[len(self.df)] = [bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume]
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        self.done = True
        self.disconnect()

app.reqHistoricalData(1, mycontract, "", "1 D", "1 min", "BID", 1, 1, False, [])

