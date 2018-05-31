# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.log.quant_logging import quant_logging as logging
from quant.config import default_config
from sqlalchemy import create_engine
from quant.dao.data_source import dataSource
import schedule
import time
import tushare as ts
from quant.dao.k_data_dao import k_data_dao
from quant.dao.index_k_data_dao import index_k_data_dao
from quant.models.logistic_regression_classifier import LogisticRegressionClassifier
from quant.models.pac_model import PACModel

PROJECT_NAME = "quant-collector"


def init_db():
    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=100, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine


def init_logger():
    # 使用单例模式保存logger
    logging.create_logger(default_config.DEBUG, PROJECT_NAME)


def training():
    pac = PACModel()
    df_index = index_k_data_dao.get_rel_price();
    df, features = k_data_dao.get_k_predict_data_with_features("600196", df_index)
    pac.training_model('600196', df, features)
    '''
    df = ts.get_hs300s()
    for code in df['code'].values:
        df_index = index_k_data_dao.get_rel_price();
        df, features = k_data_dao.get_k_predict_data_with_features(code, df_index)

        pac = PACModel()
        pac.training_model(code, df, features)
    '''


if __name__ == '__main__':
    init_logger()
    init_db()

    training()
    # schedule.every().day.at("15:30").do(k_data.collect_hs300_daily)


    while True:
        schedule.run_pending()
        time.sleep(1)
