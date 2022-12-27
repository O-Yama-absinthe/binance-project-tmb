# Импорт библиотек 
import asyncio
from binance import AsyncClient
import configparser
import pandas as pd
from datetime import datetime

# Загрузка ключей из файла config


async def main():
    config = configparser.ConfigParser()
    config.read_file(open('secret.cfg'))
    test_api_key = config.get('BINANCE', 'API_KEY')
    test_secret_key = config.get('BINANCE', 'SECRET_KEY')
    print(datetime.now())
    client = await AsyncClient.create(test_api_key, test_secret_key)

    info = await client.futures_exchange_info()
    symbols = []
    symbols_futures = []
    data =[]

    for n in info['symbols']:
        symbols_futures.append(n['symbol'])

    info = await client.get_exchange_info()
    for ticker in info['symbols']:
        if ('SPOT' in ticker['permissions']) & ('USDT' in ticker['quoteAsset']) & (ticker['symbol'] in symbols_futures):
            symbols.append(ticker['symbol'])
    #print(symbols)

    for symbol in symbols:
        dat=[symbol]
        klines = await client.get_historical_klines(symbol, AsyncClient.KLINE_INTERVAL_5MINUTE, "30 minutes ago UTC", "Now")
        for kline in klines:
            dat=dat+kline[1:6]
            #data.append([symbol]+[datetime.fromtimestamp(kline[0]/1000)]+kline[1:6])
#+[time.strftime('%H:%M:%S', time.gmtime(kline[7]))]
        data.append(dat)
    df = pd.DataFrame(data, columns=['symbol', 'open1', 'high1', 'low1', 'close1', 'volume1', 'open2', 'high2', 'low2', 'close2', 'volume2','open3', 'high3', 'low3', 'close3', 'volume3','open4', 'high4', 'low4', 'close4', 'volume4','open5', 'high5', 'low5', 'close5', 'volume5','open6', 'high6', 'low6', 'close6', 'volume6'])
    print(df)
    print(datetime.now())
    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
