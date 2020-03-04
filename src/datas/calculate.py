import numpy as np


def calculate_ma(data):
    """ 计算周期的均线 """
    if len(data) != 20:
        raise ValueError('calculate 20 period moving average should give 20 period data!')
    return sum([d['close'] for d in data]) / 20


def calculate_LB(data):
    """ 计算布林下轨 """
    if len(data) != 20:
        raise ValueError('calculate 20 period moving average should give 20 period data!')
    last_20_weeks_close = [i['close'] for i in data]
    md = np.std(last_20_weeks_close, ddof=0)
    ma20 = calculate_ma(data)
    return ma20 - 2 * md


def calculate_UB(data):
    """ 计算布林上轨 """
    if len(data) != 20:
        raise ValueError('calculate 20 period moving average should give 20 period data!')
    last_20_weeks_close = [i['close'] for i in data]
    md = np.std(last_20_weeks_close, ddof=0)
    ma20 = calculate_ma(data)
    return ma20 + 2 * md


def calculate_vol_vol3(data):
    """ 计算"""
    if len(data) != 3:
        raise ValueError('计算前三周交易量均值，data长度不为3')
    vol= data[0]['amount']
    vol3_avg = sum([d['amount'] for d in data]) / 3
    return vol / 1000, vol3_avg / 1000