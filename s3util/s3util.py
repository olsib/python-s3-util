import os
import collections
import datetime
import mimetypes

import pytz
import boto
from boto.ec2.cloudwatch import CloudWatchConnection
from boto.s3.key import Key


class S3Util(object):

    def __init__(self,
                 aws_access_key,
                 aws_secret_access_key,
                 cloudwatch_region='us-west-2',
                 cloudwatch_namespace='',
                 s3_bucket=''):

        """
        :param aws_access_key:
        :param aws_secret_access_key:
        :param cloudwatch_region: The CloudWatch region to report metrics to.
        :type cloudwatch_region: str
        :return:
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key

        for region in boto.ec2.cloudwatch.regions():
            if region.name == cloudwatch_region:
                self.cloudwatch_region = region

        self.cloudwatch_namespace = cloudwatch_namespace
        self.s3_bucket = s3_bucket

    def get_s3_bucket(self):
        bucket_name = self.s3_bucket

        s3 = boto.connect_s3(self.aws_access_key, self.aws_secret_access_key)
        return s3.get_bucket(bucket_name)

    def set_s3_bucket(self, bucket_name):
        self.s3_bucket = bucket_name

    def save_screenshot(self, key_name, screenshot, url_expiration_seconds_from_now=None):
        if not url_expiration_seconds_from_now:
            url_expiration_seconds_from_now = datetime.timedelta(days=365).total_seconds()

        bucket = self.get_s3_bucket()
        key = bucket.new_key(key_name)

        if isinstance(screenshot, basestring):
            key.set_contents_from_string(screenshot)
        elif isinstance(screenshot, file):
            key.set_contents_from_file(screenshot)

        url = key.generate_url(
            expires_in=url_expiration_seconds_from_now,
            response_headers={'response-content-type': mimetypes.types_map['.png']}
        )

        return url

    def make_s3_url(self, s3_key, extension='.png', expiration_seconds_from_now=None):
        if not expiration_seconds_from_now:
            expiration_seconds_from_now = datetime.timedelta(days=365).total_seconds()

        if isinstance(s3_key, Key):
            key = s3_key
        else:
            key = Key(bucket=self.get_s3_bucket(), name=s3_key)

        return key.generate_url(
            expires_in=expiration_seconds_from_now,
            response_headers={'response-content-type': mimetypes.types_map[extension]}
        )

    def list_s3_files(self, folder):
        """Returns a dict of filenames -> urls."""
        bucket = self.get_s3_bucket()
        files = collections.OrderedDict()
        iterator = bucket.list(prefix=folder)
        for key in iterator:
            file_extension = os.path.splitext(key.name)[1]
            url = self.make_s3_url(key, extension=file_extension)

            # add the url to the dict by its filename
            files[os.path.basename(key.name)] = url

        return files

    def put_metric(self, name, value, timestamp=None, dimensions=None):
        """
        Add a metric to CloudWatch.

        :param name: The metric key that will be shown in CloudWatch.
        :type name: str
        :param value: The value to submit to CloudWatch.
        :type value: float|list[float]
        :param timestamp: The timestamp that should be recorded for the metric specified.
        :type timestamp: datetime
        :param dimensions: The key-value pairs to associate with the metric.
        :type dimensions: dict
        """
        if not timestamp:
            timestamp = datetime.datetime.now(pytz.utc)

        # create the cloudwatch connection
        cloudwatch = CloudWatchConnection(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region=self.cloudwatch_region
        )

        # submit the metric to cloudwatch
        cloudwatch.put_metric_data(
            self.cloudwatch_namespace,
            name,
            value=value,
            timestamp=timestamp,
            dimensions=dimensions
        )
