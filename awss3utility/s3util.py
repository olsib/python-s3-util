import os
import collections
import datetime
import pytz
import boto
from boto.ec2.cloudwatch import CloudWatchConnection
from boto.s3.key import Key


class S3Utility(object):

    def __init__(self,
                 aws_access_key,
                 aws_secret_access_key,
                 cloudwatch_region='eu-west-1',
                 cloudwatch_namespace='s3-utility',
                 s3_bucket='',
		 publish='print',
		 formatting='GB',
		 categorize=True):

        """
        :param aws_access_key:
        :param aws_secret_access_key:
        :param cloudwatch_region: The CloudWatch region to report metrics to.
        :type cloudwatch_region: str
	:param s3_bucket: Name of bucket. Leave empty if you need to list all buckets
	:type s3_bucket: str
	:param publish: Option it you want to print or publish in Cloudwatch
	:type publish: str
	:param categorize: If true will categorize according to storage class
	:type boolean
	:return:
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key

        for region in boto.ec2.cloudwatch.regions():
            if region.name == cloudwatch_region:
                self.cloudwatch_region = region

        self.cloudwatch_namespace = cloudwatch_namespace
        self.s3_bucket = s3_bucket
	self.publish = publish
	self.fmt = formatting
	self.categorize = categorize 

    def get_all_buckets(self):
	
	s3 = boto.connect_s3(self.aws_access_key, self.aws_secret_access_key)
	
	return s3.get_all_buckets()

    def publish_stats(self):
	
        s3 = boto.connect_s3(self.aws_access_key, self.aws_secret_access_key)
	
	buckets = self.get_all_buckets()
        categorize = self.categorize
	
	publish = self.publish

	for bucket in buckets:
		fmt = self.fmt
		arr = self.get_bucket_stats(bucket.name, fmt)
	 	
		if categorize:
				
			for i in range(3):
				
				cat, fsize, totfiles, lastmodified, prnt = arr[i][0],arr[i][1],arr[i][2],arr[i][3],arr[i][4]
				if publish == 'print':
					if  prnt == 1:
						p = self.print_stats(cat, bucket.name, bucket.creation_date, fsize, totfiles, lastmodified)
				else:
					if prnt == 1:
		                        	name = bucket.name,
               			        	created = bucket.creation_date,
                        			value = totfiles 
                        			publish = self.put_metric(name, value)
				
		else:
			cat, fsize, totfiles, lastmodified = arr[3][0],arr[3][1],arr[3][2],arr[3][3]		 

	                if publish == 'print':
				p = self.print_stats(cat, bucket.name, bucket.creation_date, fsize, totfiles, lastmodified)

        		else:
                        	name = bucket.name,
	                        created = bucket.creation_date,
				value = totfiles 
				publish = self.put_metric(name, value)
    
    def print_stats(self, category, name, created, filesize, totalfiles, lastmodified):
        print "{category}\t{name}\t{created}\t{filesize}\t{totalfiles}\t{lastmodified}".format(
                category = category,
                name = name,
                created = created,
                filesize = filesize,
                totalfiles = totalfiles,
                lastmodified = lastmodified,
						)
	return
	
    def get_bucket_stats(self, name, fmt):
	
	s3 = boto.connect_s3(self.aws_access_key, self.aws_secret_access_key)
	
	categorize = self.categorize
	size = size_ST = size_RD = size_STIA = 0
	totalfiles = totalfiles_ST = totalfiles_RD = totalfiles_STIA = 0
 	l=l_ST=l_RD=l_STIA = None 	
	printST=printRD=printSTIA = False 
       	lastmodified=lastmodified_ST=lastmodified_RD=lastmodified_STIA = None

	bucket = s3.get_bucket(name)
        lt =  bucket.list()
	
	array = [[0 for row in range(0,5)] for col in range (0,4)] 		
        for obj in lt:
		if categorize:
			if obj.storage_class == 'STANDARD':
	                       l_ST = [(obj.last_modified, obj)]
	                       size_ST += obj.size
        	               totalfiles_ST += 1
			       printST = True	 

			elif obj.storage_class == 'REDUCED_REDUNDANCY':
                               l_RD = [(obj.last_modified, obj)]
                               size_RD += obj.size
                               totalfiles_RD += 1
    			       printRD = True	
	
			else:
                               l_STIA = [(obj.last_modified, obj)]
                               size_STIA += obj.size
                               totalfiles_STIA += 1
                               printSTIA = True
			    	

		l = [(obj.last_modified, obj)]	
		size += obj.size
		totalfiles += 1
	
	if l is not None:
		key=sorted(l, cmp=lambda x,y: cmp(x[0], y[0]))[-1][1]
		lastmodified = key.last_modified
	if l_ST is not None:
        	key_ST=sorted(l_ST, cmp=lambda x,y: cmp(x[0], y[0]))[-1][1]
        	lastmodified_ST = key_ST.last_modified
	if l_RD is not None:	
	        key_RD=sorted(l_RD, cmp=lambda x,y: cmp(x[0], y[0]))[-1][1]
       		lastmodified_RD = key_RD.last_modified
	if l_STIA is not None:
	        key_STIA=sorted(l_STIA, cmp=lambda x,y: cmp(x[0], y[0]))[-1][1]
       		lastmodified_STIA = key_STIA.last_modified


        array[0][0] = 'STANDARD'
        array[0][1] = self.format_size(fmt, size_ST)
        array[0][2] = totalfiles_ST
        array[0][3] = lastmodified_ST
	array[0][4] = 1 if printST else 0

        array[1][0] = 'REDUCED_REDUNDANCY'
        array[1][1] = self.format_size(fmt, size_RD)
        array[1][2] = totalfiles_RD
        array[1][3] = lastmodified_RD
	array[1][4] = 1 if printRD else 0

        array[2][0] = 'STANDARD_IA'
        array[2][1] = self.format_size(fmt, size_STIA)
        array[2][2] = totalfiles_STIA
        array[2][3] = lastmodified_STIA
	array[2][4] = 1 if printSTIA else 0

        array[3][0] = 'ALL_TYPES'
        array[3][1] = self.format_size(fmt, size)
        array[3][2] = totalfiles
        array[3][3] = lastmodified
	array[3][4] = 0 if categorize else 1
	
	return array

    def format_size(self, fmt, size):
        if fmt.lower() == 'kb':
                size = "%.3f KB" % (size*1.0/1024)
        elif fmt.lower() == 'mb':
                size = "%.3f MB" % (size*1.0/1024/1024)
        else:
                size = "%.3f GB" % (size*1.0/1024/1024/1024)
	
	return size
	
    def getregions():
    	for region in dir(Location):
	       	if region[0].isupper():
      			print region

    def get_last_modified(self, name):

        s3 = boto.connect_s3(self.aws_access_key, self.aws_secret_access_key)
	
        bucket = s3.get_bucket(name)
        lt =  bucket.list()
        for obj in lt:
		key = bucket.get_key(obj.name)
		return key.last_modified


    def get_s3_bucket(self):
        bucket_name = self.s3_bucket

        s3 = boto.connect_s3(self.aws_access_key, self.aws_secret_access_key)
        return s3.get_bucket(bucket_name)

    def set_s3_bucket(self, bucket_name):
        self.s3_bucket = bucket_name

    def put_metric(self, name, value, statistics=None, timestamp=None, dimensions=None):
        """
        Add a metric to CloudWatch.

        :param name: The metric key that will be shown in CloudWatch.
        :type name: str
        :param value: The value to submit to CloudWatch.
        :type value: float|list[float]
        :param timestamp: The timestamp that should be recorded for the metric specified.
        :type timestamp: datetime
	:param value: statistics
	:type value: list or dict
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
	    statistics=statistics,	
            dimensions=dimensions
        )
