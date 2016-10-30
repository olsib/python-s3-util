import boto
from boto.s3.key import Key

from moto import mock_s3

from awss3utility import s3util


@mock_s3
def test_stats():
    bucket_obj = s3util.S3Utility(aws_secret_access_key = 'XXX', aws_access_key = 'XXX',formatting='kb')
    print=bucket_obj.publish_stats()
    pass	
