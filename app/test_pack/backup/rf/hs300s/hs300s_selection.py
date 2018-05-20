# coding=utf-8

import warnings

import tushare as ts

from app.test_pack.backup.rf.hs300s.classifier_runner import predict


def vote8(list):
    count = 0.0
    for item in list:
        if item == 1:
            count += 1

    return count / len(list) >= 0.8


def vote100(list):
    count = 0.0
    for item in list:
        if item == 1:
            count += 1

    return count / len(list) >= 1


def filter(codes):
    print(codes)
    list = []
    for code in codes:

        df_rel = ts.get_realtime_quotes(code)

        if df_rel is None:
            continue

        pre_price = float(df_rel["pre_close"].tail(1).values[0])
        price = float(df_rel["price"].tail(1).values[0])

        p_change = (price - pre_price) / pre_price
        print(p_change)
        if p_change < -0.02:
            list.append(code)
            print(p_change)

    return list


def classifier_predict8(df):
    list = []
    for code in df['code'].values:
        try:
            pred_result = predict(code)
            print(pred_result)
            rs = vote8(pred_result)
            if rs is True:
                list.append(code)
        except Exception as e:
            print(e)
    return list


def classifier_predict100(df):
    list = []
    for code in df['code'].values:
        try:
            pred_result = predict(code)
            print(pred_result)
            rs = vote100(pred_result)
            if rs is True:
                list.append(code)
        except Exception as e:
            print(e)
    return list


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)

    #rs = classifier_predict100(ts.get_hs300s())

    #rs = filter(rs)

    # print(rs)

    #rs = classifier_predict8(ts.get_hs300s())
    rs= ['600009', '600019', '600036', '600048', '600104', '600153', '600196', '600309', '600390', '600482', '600519', '600547', '600549', '600585', '600690', '600741', '600887', '600900', '601012', '601155', '601318', '601601', '601888', '601958', '603799', '000060', '000063', '000333', '000568', '000768', '002230', '002310', '002415', '002456', '002601', '300003', '300124', '300136']
    rs = filter(rs)

    print(rs)
