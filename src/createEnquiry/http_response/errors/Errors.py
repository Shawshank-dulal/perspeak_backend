INVALID_HTTP_METHOD_BODY = "Body Sent In Request Was Invalid"
INVALID_HTTP_METHOD_REQUEST_TYPE = "Method Type Sent In Request Was Invalid"
BAD_REQUEST = "BAD REQUEST"


class InvalidHttpMethodError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
