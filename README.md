This is a collection of utility tools for S3 

To install the package run
- python setup.py install

To test in ipython

- from awss3utility import s3util


For size formatting you need to provide 'formatting' argument, default GB

- bucket_obj = s3util.S3Utility(aws_secret_access_key = 'XXX', aws_access_key = 'XXX',formatting='kb')
- print=bucket_obj.publish_stats()

For categorizing by Storage Type, you need to supply 'categorize' argument, which defaults True.
- bucket_obj = s3util.S3Utility(aws_secret_access_key = 'XXX', aws_access_key = 'XXX',formatting='kb',categorize=False)
- print=bucket_obj.publish_stats()

For publishing total number of files in Cloudwatch as a metric you will need to set 'publish' argument to 'cloudwatch'.
- bucket_obj = s3util.S3Utilty(aws_secret_access_key = 'XXX', aws_access_key = 'XXX', cloudwatch_namespace='s3util', cloudwatch_region='eu-west-1',formatting='mb', publish='cloudwatch' ,categorize=False)
- print = bucket_obj.publish_stats()


Work in progress
- Filter the results in a list of buckets (there's a bug with s3 bucket name characters in boto if special chars used.)
- Ability to group information by regions

- Use dynamic arrays
- Better error handling
- Multithreading for processing bucket list information quicker when large volumes of files
- Finish unit testing	

