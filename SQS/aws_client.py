## aws credentials and client to talk to aws through boto3

import os
import boto3
from dotenv import load_dotenv

load_dotenv()


class AWSClient:
    def get_client(self, service_name="sqs"):
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION")

        return boto3.client(
            service_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
