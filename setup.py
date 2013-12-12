#!/usr/bin/env python

from setuptools import setup

setup(name='dcr',
      version='0.1.4',
      description='Docker Container Start - start Docker Containers from YML',
      url='http://github.com/dhrp/docker-runner',
      author='Thatcher Peskens',
      author_email='thatcher@docker.com',
      license='MIT',
      scripts=['dcr'],
      install_requires=[
          'docker-py==0.2.2',
          'simplejson',
          'jsonpath_rw',
          'pyyaml',
          'redis',
          'bgtunnel'
      ],
      dependency_links=[
          'https://github.com/dotcloud/docker-py/tarball/master#egg=docker-py-0.2.2'
      ],
      zip_safe=False)

