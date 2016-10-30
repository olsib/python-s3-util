from setuptools import setup, find_packages

args = dict(
    name='PythonS3Util',
    version='1.0',
    packages=find_packages(exclude=("test",))
)

setup(**args)
