import numpy as np


def calculate_ma20(data):
    """ 根据传入的data计算ma20,这个data是原始data（字典的列表）"""
    ma20 = 0
    for d in data:
        ma20 += d['close']
    ma20 = ma20 / 20
    return ma20


def calculate_DN(data):
    """ 计算data中的布林下轨 """
    last_20_weeks_close = [i['close'] for i in data]
    md = np.std(last_20_weeks_close, ddof=0)
    ma20 = calculate_ma20(data)
    return ma20 - 2 * md


def calculate_UN(data):
    """ 计算data中的布林上轨 """
    last_20_weeks_close = [i['close'] for i in data]
    md = np.std(last_20_weeks_close, ddof=0)
    ma20 = calculate_ma20(data)
    return ma20 + 2 * md


def calculate_vol_vol3(data):
    if len(data) != 3:
        raise Exception('计算前三周交易量均值，data长度不为3')
    vol, vol3 = data[0]['amount'], 0
    for d in data:
        vol3 += d['amount']
    vol3_avg = vol3 / 3
    return vol / 1000, vol3_avg/1000