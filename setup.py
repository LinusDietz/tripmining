from setuptools import setup, find_packages

setup(
    name='tripmining',
    version='0.4.2',
    include_package_data=True,
    packages=find_packages(include=["tripmining.model", "tripmining.geo", "tripmining.preprocessing",
                                    "tripmining.preprocessing.parser", "tripmining.dataset"],
                           exclude=["*.test", "*.test.*", "test.*", "test"]),
    package_data={'': ['*.csv']},
    url='https://github.com/LinusDietz/tripmining',
    license='MIT',
    author='Linus Dietz',
    author_email='linus.dietz@tum.de',
    description='A Python module for mining trips from check-in based data',
    install_requires=['geopy',
                      'scipy',
                      'pytest',
                      'xmltodict',
                      'pandas',
                      'numpy',
                      'astral',
                      'sortedcontainers',
                      'pymongo',
                      'networkx',
                      'bidict',
                      'humanfriendly']
)
