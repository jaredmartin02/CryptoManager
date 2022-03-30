import csv
import ccxt
import os
import time
binance = ccxt.binanceus()
binance.apiKey = 'trVh9Yk1Brx9FA6cAbYw1nBeS4KWpDxMR1lZtmVlcesta2wjZw4eovlTjBsulCEr'
binance.secret = 'BC3gKZaBLTNcVouDCYuXKQaS19wZ1tfsLjR8QSEz9vRaI9KL0e3uYTto9UBW6Hst'
binance.enableRateLimit = True


class Prices:
    symbols = ['BTC', 'ETH', 'CRV', 'ONE', 'MATIC', 'SUSHI', 'ADA', 'SOL', 'FTM', 'ATOM', 'LINK', 'BNB', 'VET', 'YFI',
               'HBAR', 'ALGO', 'DOT', 'MANA', 'XTZ', 'AVAX', 'ENJ', 'XLM', 'ANKR', 'GRT', 'HNT', 'STORJ', 'ZEC', 'OMG',
               'EGLD', 'BAT', 'COMP', 'LTC', 'AMP', 'AXS', 'VTHO', 'BCH', 'FIL', 'NANO', 'RVN', 'EOS', 'ZIL', 'AAVE',
               'MKR', 'UNI', 'OXT', 'ZRX', 'BAND', 'NEO', 'ICX', 'WAVES', 'QTUM', 'ZEN', 'ETC', '1INCH', 'REP', 'KNC',
               'DASH', 'CTSI', 'ONT', 'PAXG']
    timeFrames = ['1d', '4h', '1h', '30m', '15m']

    def __init__(self):
        pass

    def getCoinData(self, coin, timeframe):
        data = []
        rawData = binance.fetch_ohlcv(coin + '/USD', timeframe)
        for i in rawData:
            data.append(i[1:])
        return data

    def getFullData(self):
        data = {}
        for i in self.symbols:
            data[i] = {}
        for s in self.symbols:
            for t in self.timeFrames:
                data[s][t] = binance.fetch_ohlcv(s + '/USD', t)
        return data

    def writeFile(self, filePath, data):
        with open(filePath, 'w') as file:
            writer = csv.writer(file)
            for s in self.symbols:
                writer.writerow([s])
                writer.writerow(['1d'])
                writer.writerows(data[s]['1d'])
                writer.writerow(['4h'])
                writer.writerows(data[s]['4h'])
                writer.writerow(['1h'])
                writer.writerows(data[s]['1h'])
                writer.writerow(['30m'])
                writer.writerows(data[s]['30m'])
                writer.writerow(['15m'])
                writer.writerows(data[s]['15m'])
            writer.writerow(['end'])

    def readFile(self, filePath):
        rawData = []
        data = {}
        currentS = 0
        for k in self.symbols:
            data[k] = {}
        with open(filePath, 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                rawData.append(line)
            for i in range(len(rawData)):
                if rawData[i][0] == self.symbols[currentS]:
                    start = i+2
                if rawData[i][0] == '4h':
                    data[self.symbols[currentS]]['1d'] = rawData[start+1:i]
                    start = i
                if rawData[i][0] == '1h':
                    data[self.symbols[currentS]]['4h'] = rawData[start+1:i]
                    start = i
                if rawData[i][0] == '30m':
                    data[self.symbols[currentS]]['1h'] = rawData[start+1:i]
                    start = i
                if rawData[i][0] == '15m':
                    data[self.symbols[currentS]]['30m'] = rawData[start+1:i]
                    start = i
                if currentS != len(self.symbols)-1 and rawData[i][0] == self.symbols[currentS+1]:
                    data[self.symbols[currentS]]['15m'] = rawData[start+1:i]
                    start = i
                    currentS += 1
                elif rawData[i][0] == 'end':
                    data[self.symbols[currentS]]['15m'] = rawData[start+1:i]
        return data

    def updateFile(self, filePath, write):
        data = {}
        for k in self.symbols:
            data[k] = {}
        readData = self.readFile(filePath)
        newData = self.getFullData()
        print(len(readData['BTC']['1d']))
        for s in self.symbols:
            for t in self.timeFrames:
                for i in readData[s][t]:
                    if i[0] == str(newData[s][t][0][0]):
                        data[s][t] = readData[s][t][:readData[s][t].index(i)]+newData[s][t]
        if '15m' not in data[self.symbols[0]]:
            print('Not all prices could not be updated, there is a gap between historic data and current data')
        elif write == True:
            self.writeFile(filePath, data)
            print('New file written')
            print('length of 1 Day history:', len(self.readFile(filePath)['BTC']['1d']))
            print('length of 4 Hour history:', len(self.readFile(filePath)['BTC']['4h']))
            print('length of 1 Hour history:', len(self.readFile(filePath)['BTC']['1h']))
            print('length of 30 Minute history:', len(self.readFile(filePath)['BTC']['30m']))
            print('length of 15 Minute history:', len(self.readFile(filePath)['BTC']['15m']))
        return data


if __name__ == '__main__':
    prices = Prices()
    fileName = os.path.join('../data', 'test.csv')
    #prices.writeFile(fileName, prices.getFullData())
    os.chdir('../data')

    prices.updateFile('test.csv', True)
    # prices.updateFile('test.csv', True)
    #print(prices.readFile('test.csv')['ETH']['15m'][-1])

    #while True:
        #pass
        #prices.updateFile('test.csv', True)
        #os.system('git commit -am "updating price history"')
        #os.system('git push origin main')
        #time.sleep(86400)
        #time.sleep(60)