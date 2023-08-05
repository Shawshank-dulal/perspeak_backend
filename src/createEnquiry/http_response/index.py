import json
from .errors.Errors import InvalidHttpMethodError, INVALID_HTTP_METHOD_REQUEST_TYPE, INVALID_HTTP_METHOD_BODY


def validate_httpMethod(event):
    if event['httpMethod'] != 'POST':
        raise InvalidHttpMethodError(INVALID_HTTP_METHOD_REQUEST_TYPE)
    if ('body' not in event):
        raise InvalidHttpMethodError(INVALID_HTTP_METHOD_BODY)

    return True


def generate_error_response(status_code, message):

    return {
        "statusCode": status_code,
        'headers': {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Headers":"*",
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Methods":"*",
            "Accept":"*/*"
        },
        "isBase64Encoded": False,
        "body": json.dumps(message)
    }


def generate_success_response(status_code, params):
    return {
        'statusCode': status_code,
        'headers': {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Headers":"*",
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Methods":"*",
            "Accept":"*/*"
        },
        "isBase64Encoded": False,
        'body': json.dumps(params)
    }
