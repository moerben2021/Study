import os.path

import ccxt
import pandas as pd
from pathlib import Path
import time


def get_history_kline(path, exchange, symbols, intervals, start_time, end_time):
    """
    获取历史K线数据
    """
    # 创建目录
    path = Path(path, exchange.id)
    if path.exists() is False:
        path.mkdir()
    path = Path(path, 'spot')
    if path.exists() is False:
        path.mkdir()
    path = Path(path, str(pd.to_datetime(start_time).date())+'_'+str(pd.to_datetime(end_time).date()))
    if path.exists() is False:
        path.mkdir()

    # 获取历史数据并保存
    for symbol in symbols:
        for interval in intervals:
            # 数据文件名称
            symbolname = symbol.replace("/", "")
            filename = Path(path, symbolname + '_' + interval + '.csv')
            # 文件已存在，不再重复下载
            if filename.exists():
                continue

            # symbol每种interval的多时间段K线List
            df_list = []
            # 按ISO 8601标准计算timestamp
            start_time_since = exchange.parse8601(start_time)

            while True:
                # 获取K线数据
                df = exchange.fetch_ohlcv(symbol=symbol, timeframe=interval, since=start_time_since, limit=1000)
                # List 转为 pd.DataFrame
                df = pd.DataFrame(df, dtype=float)
                # timestamp 转为 datetime
                # df['candle_begin_time'] = pd.to_datetime(df[0], unit='ms')
                # 当前时间段K线加入List中
                df_list.append(df)

                # 为下一时间段K线做准备。取出最后一条K线的timestamp值，并转换为datetime
                t = pd.to_datetime(df.iloc[-1][0], unit='ms')
                start_time_since = exchange.parse8601(str(t))

                # 判断是否挑出循环：最后一行时间超过end_time或者获取记录数小于等于1条
                if t >= pd.to_datetime(end_time) or df.shape[0] <= 1:
                    print('抓取完所需数据，或抓取至最新数据，完成抓取任务，退出循环')
                    break

                # 抓取间隔需要暂停2s，防止抓取过于频繁
                print('Download ', symbol, interval, str(t), ' done')
                time.sleep(2)

            # 合并List数据
            df = pd.concat(df_list, ignore_index=True)
            # 列的重命名
            df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                               3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名
            # timestamp转为datetime并使用新列存储
            df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
            # 重新整理表格列顺序
            df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

            # 选取数据时间段
            # df = df[df['candle_begin_time'].dt.date == pd.to_datetime(start_time).date()]
            df = df[df['candle_begin_time'].dt.date >= pd.to_datetime(start_time).date()]
            df = df[df['candle_begin_time'].dt.date <= pd.to_datetime(end_time).date()]

            # 去重、排序、重置索引
            df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
            df.sort_values('candle_begin_time', inplace=True)
            df.reset_index(drop=True, inplace=True)

            # 保存
            df.to_csv(filename, index=False)
    return


if __name__ == '__main__':
    # 交易所
    exchange = ccxt.binance({
        'proxies': {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
    })
    # 交易对
    symbols = ['BTC/USDT', 'ETH/USDT', 'EOS/USDT', 'LTC/USDT', 'BNB/USDT']
    # 起始时间 & 结束时间
    start_time = '2022-01-01 00:00:00'
    end_time = '2022-11-10 23:59:59'
    # K线间隔类型
    intervals = ['5m', '15m']
    # 数据根目录，建议使用PathLib库，增加平台适应性
    path = Path('D:/data/k/regular')
    # 调用历史数据下载函数
    get_history_kline(path, exchange, symbols, intervals, start_time, end_time)
