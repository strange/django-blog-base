#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='blog_base', version='0.1',
      description='Simple reusable Django blog app',
      author='Gustaf Sjöberg', author_email='gs@distrop.com',
      packages=['blog_base', 'blog_base.templatetags'])
