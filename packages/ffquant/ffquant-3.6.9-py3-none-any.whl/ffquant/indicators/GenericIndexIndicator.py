import pytz
from datetime import datetime, timedelta
import backtrader as bt
from ffquant.utils.Logger import stdout_log
from ffquant.indicators.IndexListIndicator import IndexListIndicator
import os

__ALL__ = ['GenericIndexIndicator']

class GenericIndexIndicator(IndexListIndicator):
    params = (
        ('url', os.getenv('INDEX_LIST_URL', default='http://192.168.25.127:8285/index/list')),
        ('symbol', 'CAPITALCOM:HK50'),  # 默认值，可外部覆盖
        ('max_retries', 10),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1),
        ('test', None),
        ('debug', None),
        ('type', None),  # 默认 None，需外部指定
        ('key_list', None),  # 默认 None，需外部指定
        ('indicator_name', None),  # 默认 None，需外部指定
    )

    def __init__(self):
        super().__init__()

        # 检查必须提供的参数
        if self.p.indicator_name is None:
            raise ValueError("indicator_name parameter must be provided and cannot be None")
        if self.p.type is None:
            raise ValueError("type parameter must be provided and cannot be None")
        if self.p.key_list is None:
            raise ValueError("key_list parameter must be provided and cannot be None")

    def determine_final_result(self):
        for line_name in self.lines.getlinealiases():
            getattr(self.lines, line_name)[0] = float('-inf')
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        cache_key_time = current_bar_time
        if current_bar_time.second != 0:
            cache_key_time = current_bar_time.replace(second=0, microsecond=0)
        cache_key_time_str = cache_key_time.strftime('%Y-%m-%d %H:%M:%S')

        result = None
        if cache_key_time_str in self.cache:
            result = self.cache[cache_key_time_str]

        if result is not None:
            for key, value in dict(result).items():
                if key in self.lines.getlinealiases():
                    line = getattr(self.lines, key)
                    if isinstance(value, (float, int)):
                        line[0] = float(value)
            return result.get('closeTime', 0)
        else:
            return 0

    def prepare_params(self, start_time_str, end_time_str):
        params = {
            'symbol': self.p.symbol,
            'type': self.p.type,
            'key_list': self.p.key_list,
            'startTime': start_time_str,
            'endTime': end_time_str
        }

        return params