import os
from setuptools import setup

this_dir = os.path.dirname(__file__)
long_description = "\n" + open(os.path.join(this_dir, 'README.md')).read()

setup(
    name='pyteamcity',
    version='0.0.0',
    description='Use the TeamCity REST API from Python',
    long_description=long_description,
    url='https://github.com/SurveyMonkey/pyteamcity',
    author='Marc Abramowitz',
    author_email='marca@surveymonkey.com',
    py_modules=['pyteamcity'],
    zip_safe=False,
    install_requires=['requests'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
