from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'boto>=2.38.0,<3.0.0',
    'boto3>=1.2.3,<1.3.0',
]

TEST_REQUIRES = [
#    'moto>=0.4.19,<0.5.0',
#    'pytest>=2.8.5,<2.9.0',
]

setup(
    name='PythonS3Utility',
    version='0.1',
    author="Olsi Birbo",
    author_email="olsi.birbo@gmail.com",
    description="collection of AWS useful functions for S3",
    url='https://github.com/olsib/python-s3-util',
    packages=find_packages(exclude=['test']),
    install_requires=INSTALL_REQUIRES + TEST_REQUIRES, # not entirely corect but gets tests with moto working
    # test_require=TEST_REQUIRES,
)

