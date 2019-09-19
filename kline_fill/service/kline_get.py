import gzip
import json
import requests
import websocket


def kline_with_ws(uri: str, request_data: dict) -> dict:
    ws = websocket.create_connection(uri)
    request_data = json.dumps(request_data)
    ws.send(request_data)
    res = ws.recv()
    try:
        res = json.loads(res)
    except UnicodeDecodeError:
        res = json.loads(gzip.decompress(res).decode("utf-8"))
    ws.close()
    return res


def kline_with_api(uri: str, request_data: dict, headers: str = None) -> dict:
    if headers:
        headers = json.loads(headers)
    res = requests.get(uri, params=request_data, headers=headers)
    return json.loads(res.text)


def kline_restful(info, status_code, data=None):
    code_info = {
        2000: 'ok',
        2001: 'Normal process,but could not get data!',
        4000: 'The server could not process the request, likely due to an invalid argument.',
        5000: 'An unexpected server issue was encountered.'

    }
    info['status'] = status_code
    result = {
        "kline_info": info,
        "msg": code_info[status_code],
        "data": data
    }
    return result
