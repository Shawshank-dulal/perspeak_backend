import boto3
from botocore.exceptions import ClientError
import os
from utils.index import get_serilized_list, dynamo_obj_to_python_obj

ENVIRONMENT=os.environ.get('ENV','staging')
ENV='testing'
ERROR_HELP_STRINGS = {
    # Common Errors
    'InternalServerError': 'Internal Server Error, generally safe to retry with exponential back-off',
    'ProvisionedThroughputExceededException': 'Request rate is too high. If you\'re using a custom retry strategy make sure to retry with exponential back-off.' +
                                              'Otherwise consider reducing frequency of requests or increasing provisioned capacity for your table or secondary index',
    'ResourceNotFoundException': 'One of the tables was not found, verify table exists before retrying',
    'ServiceUnavailable': 'Had trouble reaching DynamoDB. generally safe to retry with exponential back-off',
    'ThrottlingException': 'Request denied due to throttling, generally safe to retry with exponential back-off',
    'UnrecognizedClientException': 'The request signature is incorrect most likely due to an invalid AWS access key ID or secret key, fix before retrying',
    'ValidationException': 'The input fails to satisfy the constraints specified by DynamoDB, fix input before retrying',
    'RequestLimitExceeded': 'Throughput exceeds the current throughput limit for your account, increase account level throughput before retrying',
}
def setEnv(env):
    global ENVIRONMENT
    ENVIRONMENT=env


def create_dynamodb_client(region="us-east-1"): 
    print(ENVIRONMENT)
    if ENVIRONMENT=="testing":
        return boto3.client("dynamodb", region_name=region,endpoint_url='http://localhost:8000')
    else:
        return boto3.client("dynamodb", region_name=region)


def handle_error(error):
    error_code = error.response['Error']['Code']
    error_message = error.response['Error']['Message']

    error_help_string = ERROR_HELP_STRINGS[error_code]

    print('[{error_code}] {help_string}. Error message: {error_message}'
          .format(error_code=error_code,
                  help_string=error_help_string,
                  error_message=error_message))
    
def execute_query(dynamodb_client, input):
    try:
        response = dynamodb_client.query(**input)
        print("Query successful.")
        return response
        # Handle response
    except ClientError as error:
        handle_error(error)
    except BaseException as error: 
        print("Unknown error while querying: " + error.response['Error']['Message'])


def insert(params):
    TABLE=f"{ENVIRONMENT}-perspeak-inquiry"
    client=create_dynamodb_client()
    return client.put_item(
        TableName=TABLE,
        Item=params
    )
# def updateUsername(obj, username):
#     print(obj)
#     TABLE=f"{ENVIRONMENT}-user-profile"
#     client=create_dynamodb_client()
#     primary_key = {
#     'partition_key_name': f'user#{obj["email"]["S"]}',
#     'sort_key_name': f'username#{obj["username"]["S"]}'  # Skip this line if your table doesn't have a sort key
#     }
#     attribute_to_update = 'username'
#     new_value = username

#     response = client.update_item(
#         TableName=TABLE,
#         Key=primary_key,
#         UpdateExpression='SET #attr = :val',
#         ExpressionAttributeNames={'#attr': attribute_to_update},
#         ExpressionAttributeValues={':val': {'S': new_value}}  # Adjust the type (S, N, etc.) as per your data
#     )

#     print("UpdateItem succeeded:", response)

    

def getUserDetailsById(email):
    
    TABLE=f"{ENVIRONMENT}-user-profile"
    PK=f"user#{email}"

    params={
        "TableName":TABLE,
        "KeyConditionExpression": "#user_id = :user_id",
        "ExpressionAttributeNames": {"#user_id":"pk"},
        "ExpressionAttributeValues": {":user_id": {"S":PK}}
    }
    client=create_dynamodb_client()
    db_user=execute_query(client,params)

    #checking if user exists
    if len(db_user["Items"])>0:
        db_user=db_user["Items"][0]
        return dynamo_obj_to_python_obj(db_user)
    else:
        return {}


def get_affilate_based_on_affilate_id(affilate_id):
    print('getting affiliate based on id')
    PK=f"aff#{affilate_id}"

    TABLE=f"{ENVIRONMENT}-user-profile"
    UserAffilateSecondaryIndex="UserAffilateSecondaryIndex"
    params={
        "TableName":TABLE,
        "IndexName":UserAffilateSecondaryIndex,
        "KeyConditionExpression": "#user_id = :user_id",
        "ExpressionAttributeNames": {"#user_id":"GSIAffilateId"},
        "ExpressionAttributeValues": {":user_id": {"S":PK}}
    }

    client=create_dynamodb_client()
    db_user=execute_query(client,params)['Items']
    return get_serilized_list(db_user)


def validate_uniquness_username_email(email,username):
    PK=f"user#{email}"
    SK=f"username#{username}"

    TABLE=f"{ENVIRONMENT}-user-profile"

    params={
        "TableName":TABLE,
        "KeyConditionExpression": "#user_id = :user_id",
        "ExpressionAttributeNames": {"#user_id":"pk"},
        "ExpressionAttributeValues": {":user_id": {"S":PK}}
    }

    client=create_dynamodb_client()
    db_user=execute_query(client,params)
    print(db_user)
    #checking if user exists
    if len(db_user["Items"])>0:
        db_user=db_user["Items"][0]
        return {"valid_email_username":False}
    else:
        return {"valid_email_username":True}
