This is a collection of utility tools for S3 

To install
python setup.py install

To test in ipython

from awss3utility import s3util


For size formatting you need to provide 'formatting' argument, default GB
bucket_obj = s3util.S3Utility(aws_secret_access_key = 'XXX', aws_access_key = 'XXX', cloudwatch_namespace='s3util', cloudwatch_region='eu-west-1',formatting='kb',publish='cloudwatch')

print=bucket_obj.publish_stats()


For size formatting you need to provide 'formatting' argument, default GB
bucket_obj = s3util.S3Utility(aws_secret_access_key = 'XXX', aws_access_key = 'XXX',formatting='kb')

print=bucket_obj.publish_stats()
STANDARD        dri_stream 2016-02-05T12:52:35.000Z        6.377 KB        1       2016-10-29T06:53:55.000Z
REDUCED_REDUNDANCY      dridrugs_stream 2016-02-05T12:52:35.000Z        14.046 KB       1       2016-10-29T14:20:13.000Z
STANDARD_IA     dri_stream 2016-02-05T12:52:35.000Z        117.558 KB      1       2016-10-29T14:17:35.000Z
STANDARD        opsworks    2016-08-04T08:46:51.000Z        1.620 KB        1       2016-08-04T11:36:19.000Z

For categorizing by Storage Type, you need to supply 'category' argument, which defaults True.
bucket_obj = s3util.S3Utility(aws_secret_access_key = 'XXX', aws_access_key = 'XXX',formatting='kb',categorize=False)

print=bucket_obj.publish_stats()
ALL_TYPES       dri_stream 2016-02-05T12:52:35.000Z        137.980 KB      3       2016-10-29T14:17:35.000Z
ALL_TYPES       opsworks    2016-08-04T08:46:51.000Z        1.620 KB        1       2016-08-04T11:36:19.000Z

For publishing total number of files in Cloudwatch as a metric you will need to specify the cloudwatch namespace and region.
bucket_obj = s3util.S3Utilty(aws_secret_access_key = 'XXX', aws_access_key = 'XXX', cloudwatch_namespace='s3util', cloudwatch_region='eu-west-1',formatting='mb',categorize=False)
print = bucket_obj.publish_stats()


Work in progress
- Filter the results in a list of buckets
- Ability to group information by regions
- Multithreading for processing bucket list information quicker when large volumes of files
- Add testing

