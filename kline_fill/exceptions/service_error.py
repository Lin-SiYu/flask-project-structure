from enum import unique

from .error_core import ErrorCore


@unique
class ServiceError(ErrorCore):
    '''
    defined serivce errors
    '''

    NO_AUTH = 0
    EXPIRE = 1
    REVOKED = 2
    INVALID_HEADER_ERROR = 3
    INVALID_SIGNATURE_ERROR = 4
    METHOD_NOT_ALLOWED = 5

    USER_ALREADY_EXISTS = 200000
    USER_NOT_EXISTS = 200001
    WRONG_CREDENTIALS = 200002
    WRONG_INVITED_CODE = 200003
    PASSWORD_INCONSISTENT = 200004
    NICK_NAME_ALREADY_EXISTS = 200005
    PASSWORD_NOT_SET = 200006
    MISSING_REQUIRED_PARAMETER = 200007
    VALUE_TOO_LONG = 200008
    VALUE_TOO_SHORT = 200009
    PAY_PASSWORD_NOT_SET = 200010
    TWO_STEP_KEY_ALREADY_EXISTS = 200011
    TWO_STEP_CODE_ERROR = 200012
    TWO_STEP_NOT_SET = 200013
    TWO_STEP_KEY_EXPIRED = 200014
    TWO_STEP_SET_FAILED = 200015
    UNBIND_TWO_STEP_USER_ERROR = 200016
    UNBIND_TWO_STEP_PAYPWD_ERROR = 200017
    IDCARD_TWO_ELEMENTS_ALREADY_FINISHED = 200018
    IDCARD_TWO_ELEMENTS_REQUEST_OUT_OF_LIMIT = 200019
    IDCARD_TWO_ELEMENTS_AUTH_FAILED = 200020
    IDCARD_TWO_ELEMENTS_HASNOT_FINISHED = 200021

    ADVANCED_AUTH_HASNOT_FINISHED = 201000
    ADVANCED_AUTH_ALREADY_FINISHED = 201001
    ADVANCED_AUTH_FAILED = 201002

    UNBIND_TWO_STEP_TIME_LESS_THAN_24_HOURS = 202000

    GOODS_REMOVE_FROM_SHELVES = 210000
    GOODS_SELL_END = 210001

    WAITING_FOR_TRADING = 220000
    TRANSACTION_NOT_CREATED = 220001
    LACK_OF_STOCK = 220002
    PURCHASE_OUT_OF_LIMIT = 220003
    TRADE_TIME_OUT = 220004
    BALANCE_NOT_ENOUGH = 220005
    REFUSE_PAY = 220006
    PAY_PASSWORD_NOT_PROVIDE = 220007
    CAN_NOT_PAY_FOR_OTHERS = 220008
    PAY_PASSWORD_WRONG = 220009

    WITHDRAW_AMOUNT_EXCEED_MAX = 230000
    WITHDRAW_AMOUNT_LESS_THAN_MIN = 230001
    POUNDAGE_NOT_ENOUGH = 230002

    WITHDRAW_PAYPWD_CHECK_FAILED = 231002
    WITHDRAW_TWO_STEP_CHECK_FAILED = 231003

    DATA_NOT_COMPLETE = 300000
    RECORD_NOT_FOUND = 300001
    PARAMS_SHOULD_BE_COMPLETE = 300002
    NO_FOLLOWINGS = 300003
    DO_NOT_REPEAT = 300004
    INVALID_OPERATION = 300005
    DATA_IS_EXISTS = 300006
    IMAGE_FORMAT_NOT_MATCH = 300007
    INVALID_PHONE = 300008
    INVALID_EXPERIENCE_TYPE = 300009
    INVALID_MAIL = 300010
    FILE_TOO_LARGE = 300011
    GEN_IMG_ERR = 300012
    CAN_NOT_CANCEL_FOLLOW = 300013
    PLEASE_TRY_LATER = 300014
    WALLET_ADDRESS_ALREADY_EXISTS = 300015
    IDCARD_ALREADY_EXISTS = 300016

    KV_NOT_EXIST = 400001

    SMS_SENDER_ERR = 500000
    SMS_CHANNEL_CLOSED = 500001
    SMS_SENDER_LIMIT = 500002
    SMS_CODE_EXPIRE = 500003
    SMS_CODE_NOT_CORRECT = 500004
    FACE_AUTH_ERR = 500005
    ID_NUM_HAS_BEEN_USED = 500006
    MOBILE_NUMBER_ILLEGAL = 500007
    BUSINESS_LIMIT_CONTROL = 500008
    UPYUN_UPLOAD_FILE_ERR = 500020

    GEETEST_INIT_EXPIRE = 510000
    GEETEST_NOT_PASS = 510001

    DATABASE_ERROR = 600000
    TASK_SUSPEND = 600001

    IDCARD_NUM_ERR = 700000
    AUTHENTICATION_EXISTS = 700005
    NO_AUTHENTICATION = 700006

    UNKNOWN = 900001

    def descriptions(self, error, *context):
        '''
        generate error desc
        :params error: ServiceError object
        :returns: description with string for error
        '''

        _descriptions = {
            'NO_AUTH': 'Insufficient permissions',
            'EXPIRE': 'Authorization has expired.',
            'INVALID_HEADER_ERROR': 'Invalid Authorization header.',
            'INVALID_SIGNATURE_ERROR': 'Invalid signature error.',
            'METHOD_NOT_ALLOWED': 'The method is not allowed for the requested URL.',

            'MISSING_REQUIRED_PARAMETER': 'Missing required parameter: {}',
            'REVOKED': 'Token has been revoked',
            'RECORD_NOT_FOUND': '{} not found',
            'DATA_NOT_COMPLETE': 'data not complete: {}',
            'KV_NOT_EXIST': 'k-v not exist: {}',
            'DATA_IS_EXISTS': '{} is exists',
            'IMAGE_FORMAT_NOT_MATCH': 'Image format does not match',
            'INVALID_PHONE': 'Invalid phone number',
            'VALUE_TOO_LONG': '[{}] value is too long, limited as {}',
            'VALUE_TOO_SHORT': '[{}] value is too short, at least {}',
            'PAY_PASSWORD_NOT_SET': 'Pay password not set',
            'INVALID_EXPERIENCE_TYPE': 'Invalid {}',
            'INVALID_MAIL': 'Invalid mail',
            'FILE_TOO_LARGE': 'The transmitted data exceeds the limit',
            'GEN_IMG_ERR': 'Gen image error',
            'CAN_NOT_CANCEL_FOLLOW': 'The founder can\'t unfollow the community',
            'PLEASE_TRY_LATER': 'Please try later',
            'WALLET_ADDRESS_ALREADY_EXISTS': 'Wallet address already exists',
            'IDCARD_ALREADY_EXISTS': 'IDCard already exists',
            'TWO_STEP_KEY_ALREADY_EXISTS': 'Two step key already exists',
            'TWO_STEP_CODE_ERROR': 'Two step code error',
            'TWO_STEP_NOT_SET': 'Two step not set',
            'TWO_STEP_KEY_EXPIRED': 'Two step key expired',
            'TWO_STEP_SET_FAILED': 'Two step set failed',
            'UNBIND_TWO_STEP_USER_ERROR': 'Account check failed',
            'UNBIND_TWO_STEP_PAYPWD_ERROR': 'Pay password check failed',
            'IDCARD_TWO_ELEMENTS_ALREADY_FINISHED': 'IDCard two elements already finished',
            'IDCARD_TWO_ELEMENTS_REQUEST_OUT_OF_LIMIT': 'IDCard two elements request out of limit',
            'IDCARD_TWO_ELEMENTS_AUTH_FAILED': 'IDCard two elements auth failed',
            'IDCARD_TWO_ELEMENTS_HASNOT_FINISHED': 'IDCard two elements auth has not finished yet',

            'ADVANCED_AUTH_HASNOT_FINISHED': 'Advanced auth has not finished yet',
            'ADVANCED_AUTH_ALREADY_FINISHED': 'Advanced auth has already finished',
            'ADVANCED_AUTH_FAILED': 'Advanced auth failed',

            'UNBIND_TWO_STEP_TIME_LESS_THAN_24_HOURS': 'Unbind two step time less than 24 hours',

            'GOODS_REMOVE_FROM_SHELVES': 'Goods has already been removed from shelves',
            'GOODS_SELL_END': 'Goods selling end',

            'WAITING_FOR_TRADING': 'Waiting for trading',
            'TRANSACTION_NOT_CREATED': 'Trading failed. Transaction not created',
            'LACK_OF_STOCK': 'Trading failed. Lack of stock',
            'PURCHASE_OUT_OF_LIMIT': 'Trading failed. Purchase out of limit',
            'TRADE_TIME_OUT': 'Query time out',
            'BALANCE_NOT_ENOUGH': 'Balance not enough',
            'REFUSE_PAY': 'Not allow to pay',
            'PAY_PASSWORD_NOT_PROVIDE': 'Transaction failed. Must provide pay password',
            'CAN_NOT_PAY_FOR_OTHERS': 'User can not pay for others',
            'PAY_PASSWORD_WRONG': 'Pay password wrong',

            'WITHDRAW_AMOUNT_EXCEED_MAX': 'Withdraw amount exceed maximum asset',
            'WITHDRAW_AMOUNT_LESS_THAN_MIN': 'Withdraw amount less than minimum asset',
            'POUNDAGE_NOT_ENOUGH': 'Poundage not enough',

            'WITHDRAW_PAYPWD_CHECK_FAILED': 'Withdraw pay password check failed',
            'WITHDRAW_TWO_STEP_CHECK_FAILED': 'Withdraw two step code check failed',

            'PARAMS_SHOULD_BE_COMPLETE': 'Params should be complete',
            'NO_FOLLOWINGS': 'You have no followings',
            'DO_NOT_REPEAT': 'Do not repeat [{}]',
            'INVALID_OPERATION': 'Invalid operation:[{}]',
            'USER_ALREADY_EXISTS': 'User already exists',
            'NICK_NAME_ALREADY_EXISTS': 'Nickname {} already exists',
            'USER_NOT_EXISTS': 'User not exists',
            'WRONG_INVITED_CODE': 'Invited_code not exists',
            'PASSWORD_INCONSISTENT': 'Inconsistent password',
            'PASSWORD_NOT_SET': 'Password not set',
            'WRONG_CREDENTIALS': '{}',

            'SMS_SENDER_ERR': '{}',
            'SMS_CHANNEL_CLOSED': '[{}]-Sms channel closed',
            'SMS_SENDER_LIMIT': 'Sms sender time limit, Try after {}s',
            'SMS_CODE_EXPIRE': '[{}]-Sms code has been expire',
            'SMS_CODE_NOT_CORRECT': '[{}]-Sms code is not correct',
            'FACE_AUTH_ERR': '{}',
            'ID_NUM_HAS_BEEN_USED': 'ID number has been used',
            'MOBILE_NUMBER_ILLEGAL': 'Invalid mobile number',
            'BUSINESS_LIMIT_CONTROL': 'SmsSender limit',

            'UPYUN_UPLOAD_FILE_ERR': 'Upload file error',

            'GEETEST_INIT_EXPIRE': 'Geetest init expire',
            'GEETEST_NOT_PASS': 'Geetest not pass',

            'IDCARD_NUM_ERR': 'ID card number does not meet the specifications',
            'AUTHENTICATION_EXISTS': 'Identity authentication information already exists',
            'NO_AUTHENTICATION': 'No authentication',

            'TASK_SUSPEND': '{} has been suspend',
            'DATABASE_ERROR': '{}',

            'UNKNOWN': '{}'
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
