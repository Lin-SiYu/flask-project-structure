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
            'UNKNOWN': '{}'
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
