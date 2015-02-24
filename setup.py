import os
from setuptools import setup

this_dir = os.path.dirname(__file__)
long_description = "\n" + open(os.path.join(this_dir, 'README.md')).read()

setup(
    name='teamcity_rest_client',
    version='0.0.0',
    description='TeamCity Python REST api client',
    long_description=long_description,
    url='https://github.com/yotamoron/teamcity-python-rest-client',
    author='Yotam Oron',
    author_email='yotamoron@yahoo.com',
    py_modules=['teamcityrestapiclient'],
    zip_safe=False,
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
