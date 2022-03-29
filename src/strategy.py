import numpy as np
import pandas as pd
from ta.momentum import StochRSIIndicator as RSI
#from ta.trend import SMAIndicator as SMA
#from ta.volatility import BollingerBands as BB


class Strategy:
    def __init__(self, pfClass, exClass):
        self.pfClass = pfClass
        self.exClass = exClass

    def stochRsi(self, data):
        series = pd.Series(np.array(data)[:, 3])
        rsiObject = RSI(series, 14, 3, 3)
        rsiKList = rsiObject.stochrsi_k().to_list()
        rsiDList = rsiObject.stochrsi_d().to_list()
        return rsiKList, rsiDList