import boto3


def init_s3(region: str):
    yield boto3.client("s3", region_name=region)
