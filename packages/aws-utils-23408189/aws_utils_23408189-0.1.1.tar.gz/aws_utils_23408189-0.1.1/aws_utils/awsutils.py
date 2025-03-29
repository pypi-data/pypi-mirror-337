import boto3
from botocore.exceptions import ClientError

class AWSUtils:
    def __init__(self, region_name='us-east-1'):
        self.region_name = region_name
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        self.s3_client = boto3.client('s3', region_name=self.region_name)
        self.sns_client = boto3.client('sns', region_name=self.region_name)
    
    def table_checker(self, table_name):
        try:
            table = self.dynamodb.Table(table_name)
            if table.table_status in ["ACTIVE", "UPDATING"]:
                return True
        except ClientError:
            table_created = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST"
            )
            table_created.wait_until_exists()
            return True
        except Exception as e:
            print(e)
            return False
    
    def create_s3_bucket(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            try:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region_name}
                )
                waiter = self.s3_client.get_waiter('bucket_exists')
                waiter.wait(Bucket=bucket_name)
                return True
            except Exception as e:
                print(e)
                return False
    
    def scan_dynamo(self, payload):
        try:
            if not payload:
                return {"status": "payload_not_given"}
            
            search = payload.get("search")
            data = payload.get("data")
            
            if search not in ['user_id', 'email']:
                return {"status": False, "response": "Please provide an appropriate attribute to scan"}
            
            table = self.dynamodb.Table('user')
            filter_expression = "id = :id" if search == "user_id" else "email = :email"
            response = table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues={":id" if search == "user_id" else ":email": data}
            )
            
            return {
                "status": True if 'Items' in response else False,
                "data": response.get('Items', {})
            }
        except Exception as e:
            print(e)
            return False
    
    def send_sns_email(self, payload):
        try:
            required_keys = {"arn", "email", "subject", "msg"}
            if not payload or not required_keys.issubset(payload):
                return {"status": "payload_not_given"}
            
            self.sns_client.publish(
                TopicArn=payload["arn"],
                Message=payload["msg"],
                Subject=payload["subject"],
                MessageAttributes={
                    'email': {
                        'DataType': 'String',
                        'StringValue': payload["email"]
                    }
                }
            )
            return True
        except Exception as e:
            print(e)
            return False
