import os
import csv
import ccxt
import matplotlib.pyplot as plt
import pandas as pd
from priceHistory import Prices

#test

path = os.path.join('data', 'history.csv')

def plotBacktest(data, title, buys, sells, save):
    df = pd.DataFrame(data, columns=['open', 'high', 'low', 'close', 'volume'])
    width1, width2 = 0.9, 0.1
    up = df[df.close >= df.open]
    down = df[df.close < df.open]
    fig1 = plt.figure(figsize=(15, 8))
    for j in buys:
        plt.text(j, df.iloc[j]['low'], 'BUY')
    for k in sells:
        plt.text(k, df.iloc[k]['high'], 'SELL')
    plt.plot(buys, df.iloc[buys]['low'], linewidth=0, marker='^', color='blue')
    plt.plot(sells, df.iloc[sells]['high'], linewidth=0, marker='v', color='blue')
    plt.bar(up.index, up.close-up.open, width1, bottom=up.open, color='green')
    plt.bar(up.index, up.high-up.close, width2, bottom=up.close, color='green')
    plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color='green')
    plt.bar(down.index, down.close-down.open, width1, bottom=down.open, color='red')
    plt.bar(down.index, down.high-down.open, width2, bottom=down.open, color='red')
    plt.bar(down.index, down.low-down.close, width2, bottom=down.close, color='red')
    plt.title(title)
    plt.ylabel('USD')
    fig1.tight_layout()
    if save == True:
        plt.savefig('images/'+title+'.png')
    plt.show()

class Portfolio:
    def __init__(self, USD):
        self.holdings = {}
        self.holdings['USD'] = USD

binance = ccxt.binanceus()
binance.apiKey = 'trVh9Yk1Brx9FA6cAbYw1nBeS4KWpDxMR1lZtmVlcesta2wjZw4eovlTjBsulCEr'
binance.secret = 'BC3gKZaBLTNcVouDCYuXKQaS19wZ1tfsLjR8QSEz9vRaI9KL0e3uYTto9UBW6Hst'
binance.enableRateLimit = True
binance.load_markets()

class Exchange:

    def __init__(self, pfClass, fee):
        self.pfClass = pfClass
        self.fee = fee

    def getHistory(self, coin, timeframe):
        ohlcv = binance.fetch_ohlcv(coin+'/USD', timeframe)
        close = []
        for i in ohlcv:
            close.append(i[-2])
        return close

    def buyOrder(self, coin, price, USD):
        self.pfClass.holdings['USD'] -= USD
        self.pfClass.holdings[coin] += price*USD

    def sellOrder(self, coin, price, amount):
        if amount == -1:
            self.pfClass.holdings['USD'] += self.pfClass.holdings[coin]*price
            self.pfClass.holdings[coin] = 0
        else:
            self.pfClass.holdings['USD'] += self.pfClass.holdings[coin]*price
            self.pfClass.holdings[coin] -= amount


if __name__ == '__main__':
    portfolio = Portfolio
    exchange = Exchange(portfolio, 0.5)
    prices = Prices(5)
    data = prices.getCoinData('ADA', '1h')
    plotBacktest(data, 'ADA15m', [6, 140, 380], [50, 180, 290], True)