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
