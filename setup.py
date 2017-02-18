import os
from setuptools import setup, find_packages

version = '0.1.1'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

try:
    import pypandoc
    README = pypandoc.convert('README.md', 'rst')
    CHANGES = pypandoc.convert('CHANGES.md', 'rst')
except:
    README = read('README.md')
    CHANGES = read('CHANGES.md')

setup(
    name='pyteamcity',
    version=version,
    description='Use the TeamCity REST API from Python',
    long_description='%s\n\n%s' % (README, CHANGES),
    url='https://github.com/SurveyMonkey/pyteamcity',
    maintainer='Marc Abramowitz',
    maintainer_email='marc@marc-abramowitz.com',
    author='Yotam Oron',
    author_email='yotamoron@yahoo.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'beautifulsoup4',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
    ],
    extras_require={
        'tests': [
            'mock >= 2.0.0',
            'pytest >= 3.0.2',
            'pytest-cov >= 2.3.1',
            'responses >= 0.5.1',
        ],
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
