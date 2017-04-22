#! /usr/bin/env python
# coding: utf-8

from __future__ import (
	absolute_import,
	unicode_literals
)

import sys
import os
import unittest


def main():

	project_path = os.path.split(os.path.dirname(__file__))
	sys.path.append(project_path[0])
	test_loader = unittest.TestLoader()
	tests = test_loader.discover("tests", "*tests.py")
	result = unittest.TextTestRunner().run(tests)

	if not result.wasSuccessful():
		sys.exit(1)


if __name__ == '__main__':
	main()
