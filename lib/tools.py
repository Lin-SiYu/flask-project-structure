import datetime
import re


def kline_granularity(period):
    '''
    kline 粒度转换
    :param period: str - e.g. 1min ,1hour
    :return: 单位转换为秒制 2mon = 2*2592000
    '''
    period_num = int(re.findall(r'\d+', period)[0])
    period_unit = re.findall(r'\D+', period)[0]
    units = ['min', 'hour', 'day', 'week', 'mon', 'year']
    if period_unit not in units:
        raise Exception('Unit can not be analysed! Please check out!')
    units_multiplier = {
        'min': 60, 'hour': 3600, 'day': 86400, 'week': 604800, 'mon': 2592000, 'year': 31536000
    }
    return units_multiplier[period_unit] * period_num


def timestamp2iso(ts, tt=None, tz=datetime.timezone.utc):
    dtime = datetime.datetime.fromtimestamp(ts, tz=tz)
    iso_time = dtime.isoformat()
    # 2019-09-25T08:40:17.829317+00:00
    if tt == 'iso_8601':
        iso_time = dtime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        # 2019-09-25T17:41:49.000000Z
    return iso_time


def get_dic(values, *keys):
    '''
    e.g.
        res = get_dic(('v1', 'v2'),['k1', 'k2'])
    or
        res = get_dic(['v1', 'v2'], ['k1', 'k2'])
    {'k1': 'v1', 'k2': 'v2'}
    '''
    return dict(zip(*keys, values))
