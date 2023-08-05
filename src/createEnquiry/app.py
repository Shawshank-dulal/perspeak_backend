import os
import json
from cgi import parse_multipart, parse_header
from io import BytesIO
import base64
import datetime
from database.index import  insert
from http_response.index import  generate_error_response, generate_success_response,validate_httpMethod
from http_response.errors.Errors import InvalidHttpMethodError, BAD_REQUEST
from utils.index import generate_unique_id,python_obj_to_dynamo_obj
import time

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

def handler(event, context):
    # setEnv("testing")
    # os.environ['ENV']="testing"
    try:
        data=json.loads(event['body'])
        print(data)
        data['pk']=str(datetime.datetime.now())+"-"+str(data['fullname'])
        params = python_obj_to_dynamo_obj(data)
        print(params)
        insert(params=params)
        return generate_success_response(status_code=201, params='')
    


    except InvalidHttpMethodError as e:
        return generate_error_response(status_code=400, message={"message": e.message})
    except InvalidDataError as e:
        return generate_error_response(status_code=400, message={"message": e.message})
    except Exception as e:
        print(str(e))
        return generate_error_response(status_code=400, message={"message": BAD_REQUEST})

# print(handler({"httpMethod":"POST","body":"{\"email\": \"test_user_1111a1@gmail.com\",\"username\": \"sujan07\",\"referrer\": \"\",\"country\": \"US\"}"},{}))