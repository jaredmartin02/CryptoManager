import os
import ccxt
import csv
binance = ccxt.binanceus()
binance.apiKey = 'trVh9Yk1Brx9FA6cAbYw1nBeS4KWpDxMR1lZtmVlcesta2wjZw4eovlTjBsulCEr'
binance.secret = 'BC3gKZaBLTNcVouDCYuXKQaS19wZ1tfsLjR8QSEz9vRaI9KL0e3uYTto9UBW6Hst'
binance.enableRateLimit = True

class Prices:
    symbols = ['1INCH', 'AAVE', 'ADA', 'ALGO', 'AMP', 'ANKR', 'ANT', 'APE', 'ATOM', 'AUDIO', 'AVAX', 'AXS', 'BAND', 'BAT',
               'BCH', 'BNB', 'BTC', 'CHZ', 'COMP', 'CRV', 'CTSI', 'DAI', 'DASH', 'DOGE', 'DOT', 'EGLD', 'ENJ', 'EOS', 'ETC',
               'ETH', 'FIL', 'FLUX', 'FTM', 'GALA', 'GRT', 'HBAR', 'HNT', 'ICX', 'IOTA', 'KNC', 'KSHIB', 'LINK', 'LPT', 'LRC',
               'LTC', 'MANA', 'MATIC', 'MKR', 'NEAR', 'NEO', 'NMR', 'OGN', 'OMG', 'ONE', 'ONT', 'OXT', 'PAXG', 'POLY', 'QTUM',
               'REP', 'REQ', 'RVN', 'SLP', 'SNX', 'SOL', 'STORJ', 'SUSHI', 'TLM', 'UNI', 'VET', 'VTHO', 'WAVES', 'XLM', 'XNO',
               'XTZ', 'YFI', 'ZEC', 'ZEN', 'ZIL', 'ZRX']
    timeFrames = ['1d', '4h', '1h', '30m', '15m']

    def __init__(self):
        pass

    def getFullData(self):
        data = {}
        for i in self.symbols:
            data[i] = {}
        for s in self.symbols:
            for t in self.timeFrames:
                data[s][t] = binance.fetch_ohlcv(s + '/USD', t)
        return data

    def getCoinData(self, coin, timeFrame):
        data = []
        rawData = binance.fetch_ohlcv(coin + '/USD', timeFrame)
        for i in rawData:
            data.append(i)
        return data[:-1]

    def readCoinData(self, coin, timeFrame):
        data = []
        with open(os.path.join('data', coin, timeFrame), 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                data.append(line)
        return data

    def appendData(self, coin, timeFrame, data):
        with open(os.path.join('data', coin, timeFrame), 'a') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def updateFiles(self):
        for s in self.symbols:
            for t in self.timeFrames:
                pass


prices = Prices()
#print(prices.getCoinData('BTC', '1d'))

for s in prices.symbols:
    for t in prices.timeFrames:
        #prices.appendData(s, t+'.csv', prices.getCoinData(s, t))