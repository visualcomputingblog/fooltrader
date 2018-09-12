# -*- coding: utf-8 -*-
import enum

import pandas as pd


class TradingSignal(enum.Enum):
    TRADING_SIGNAl_LONG = 'trading_signal_long'
    TRADING_SIGNAl_SHORT = 'trading_signal_short'
    TRADING_SIGNAl_KEEP_LONG = 'trading_signal_keep_long'
    TRADING_SIGNAl_KEEP_SHORT = 'trading_signal_keep_short'


class TradingLevel(enum.Enum):
    LEVEL_1MIN = '1m'
    LEVEL_5MIN = '5m'
    LEVEL_15MIN = '15m'
    LEVEL_30MIN = '30m'
    LEVEL_1HOUR = '1h'
    LEVEL_4HOUR = '4h'
    LEVEL_1DAY = 'day'
    LEVEL_1WEEK = 'week'

    def to_second(self):
        return int(self.to_ms() / 1000)

    def to_ms(self):
        if self == TradingLevel.LEVEL_1MIN:
            return 60 * 1000
        if self == TradingLevel.LEVEL_5MIN:
            return 5 * 60 * 1000
        if self == TradingLevel.LEVEL_15MIN:
            return 15 * 60 * 1000
        if self == TradingLevel.LEVEL_30MIN:
            return 30 * 60 * 1000
        if self == TradingLevel.LEVEL_1HOUR:
            return 60 * 60 * 1000
        if self == TradingLevel.LEVEL_4HOUR:
            return 4 * 60 * 60 * 1000
        if self == TradingLevel.LEVEL_1DAY:
            return 24 * 60 * 60 * 1000
        if self == TradingLevel.LEVEL_1WEEK:
            return 7 * 24 * 60 * 60 * 1000

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.to_ms() >= other.to_ms()
        return NotImplemented

    def __gt__(self, other):

        if self.__class__ is other.__class__:
            return self.to_ms() > other.to_ms()
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.to_ms() <= other.to_ms()
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.to_ms() < other.to_ms()
        return NotImplemented


class ModelType(enum.Enum):
    TECHNICAL_MODEL = 'technical_model'
    FUNDAMENTAL_MODEL = 'fundamental_model'
    NEWS_MODEL = 'news_model'


class Model(object):
    history_data = None
    current_timestamp = None
    trading_level = None
    model_type = None

    def __init__(self, trading_level) -> None:
        self.trading_level = trading_level

    def set_history_data(self, history_data):
        self.history_data = history_data
        self.current_timestamp = history_data[-1]['timestamp']

    def append_data(self, data):
        if not self.history_data:
            self.history_data = pd.DataFrame()

        self.history_data.append(data)
        self.current_timestamp = data['timestamp']
        for decision in self.make_decision():
            yield decision

    def evaluate_fetch_interval(self, to_timestamp):
        if to_timestamp - self.current_timestamp >= self.trading_level.to_ms():
            return self.current_timestamp, to_timestamp
        return None, None

    def get_state(self):
        pass

    def make_decision(self):
        pass

    def signal_timestamp(self):
        return self.current_timestamp + TradingLevel.to_ms(self.trading_level)
