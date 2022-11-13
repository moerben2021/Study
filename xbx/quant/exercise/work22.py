'''
功能：
每天收集binance合约K线数据
永续合约+交割合约，币本位+USDT本位
交易对：btc,eth,bnb
时间周期：5m,15m
特点：
1、使用Path解决路径统一写法及目录创建
2、使用schedule实现每天定时任务
'''
import ccxt
import pandas as pd
from pathlib import Path
import time
import datetime
import schedule
import threading


def create_dir(path, level1, level2, level3):
    """
    创建目录 path/type/start_time
    :param path:    根目录
    :param level1:  'binance'
    :param level2:  'spot', 'future_usdt', 'future_coin'
    :param level3:  '2022-11-12'
    :return:
    """

    path = Path(path, level1)
    if path.exists() is False:
        path.mkdir()
    path = Path(path, level2)  # type: 'spot', 'margin', 'future'
    if path.exists() is False:
        path.mkdir()
    path = Path(path, level3)
    if path.exists() is False:
        path.mkdir()

    return path


def get_future_param(symbol, interval, startTime, endTime):
    """
    构建合约请求参数
    :param symbol:
    :param interval:
    :param startTime:
    :param endTime:
    :return:
    """
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': startTime,  # Long, ms
        'endTime': endTime,  # Long, ms
        'limit': 1000
    }
    return params


def get_yesterday_kline(path, type, exchange, symbols, intervals):
    """
    获取昨日K线数据
    :param path:
    :param type:
    :param exchange:
    :param symbols:
    :param intervals:
    :param start_time:
    :return:
    """

    if type != 'spot' and type != 'future_usdt' and type != 'future_coin':
        print('Unsupported type:', type)
        return

    # 起始时间 & 结束时间
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    start_time = str(yesterday_date) + ' 00:00:00'
    # 创建目录
    path = create_dir(path, exchange.id, type, str(yesterday_date))

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
            end_time = pd.to_datetime(start_time) + datetime.timedelta(days=1)

            while True:
                # 获取K线数据
                if (type == 'spot'):
                    df = exchange.fetch_ohlcv(symbol=symbol, timeframe=interval, since=start_time_since, limit=1000)
                elif (type == 'future_coin'):
                    para = get_future_param(symbol, interval, start_time_since, exchange.parse8601(str(end_time)))
                    df = exchange.dapiPublicGetKlines(params=para)
                    df = pd.DataFrame(df)
                elif (type == 'future_usdt'):
                    para = get_future_param(symbol, interval, start_time_since, exchange.parse8601(str(end_time)))
                    df = exchange.fapiPublicGetKlines(params=para)
                    df = pd.DataFrame(df)
                else:
                    break

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


def run():
    # 交易所
    exchange = ccxt.binance({
        'proxies': {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
    })
    # K线间隔类型
    intervals = ['5m', '15m']
    # 数据根目录，建议使用PathLib库，增加平台适应性
    path = Path('D:/data/k/regular')
    # 合约信息
    contracts = [
        {
            # U本位
            'type': 'future_usdt',
            # U本位交易对
            'symbols': ['BTCUSDT', 'BTCUSDT_221230', 'ETHUSDT', 'ETHUSDT_221230', 'BNBUSDT']
        },
        {
            # 币本位
            'type': 'future_coin',
            # 币本位合约交易对
            'symbols': ['BTCUSD_PERP', 'BTCUSD_221230', 'BTCUSD_230331',
                        'ETHUSD_PERP', 'ETHUSD_221230', 'ETHUSD_230331',
                        'BNBUSD_PERP']
        }
    ]
    # 调用历史数据下载函数
    for contract in contracts:
        get_yesterday_kline(path, contract['type'], exchange, contract['symbols'], intervals)


def run_threaded(job_func):
    """
    "启动新线程来执行定时任务"
    :return:
    """
    print('run_thread at ', datetime.datetime.now() )
    job_thread = threading.Thread(target=job_func, args=())
    job_thread.start()
    print('run_thread done at', datetime.datetime.now() )
    return


if __name__ == '__main__':
    schedule.clear()
    schedule.every().day.at("13:01:35").do(run_threaded, run).tag("day")
    while True:
        schedule.run_pending()
        time.sleep(1)
