import random
import string
import re
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from datetime import datetime, timedelta
import hashlib
import base64

def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    deserializer = TypeDeserializer()
    return {
        k: deserializer.deserialize(v) 
        for k, v in dynamo_obj.items()
    }  
  
def python_obj_to_dynamo_obj(python_obj: dict) -> dict:
    serializer = TypeSerializer()
    return {k: serializer.serialize(v) for k,v in python_obj.items()}

def get_serilized_list(item_list):
    serlilized=[]
    for data in item_list:
        serlilized.append(dynamo_obj_to_python_obj(data))
    return serlilized

def subtract_days_from_timestamp(timestamp, days_to_subtract):
    dt_object = datetime.fromtimestamp(timestamp)

    updated_dt_object = dt_object - timedelta(days=days_to_subtract)

    updated_timestamp = int(updated_dt_object.timestamp())

    return updated_timestamp

def generate_unique_id(data):
    m=hashlib.md5(data.encode('utf-8')).digest()
    val= str(base64.b64encode(m).decode())
    return val


def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
