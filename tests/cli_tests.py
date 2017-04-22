# coding: utf-8

import unittest
from click.testing import CliRunner
from moto import mock_cloudformation
from bastion.__main__ import cli


class CreateBastionTestCase(unittest.TestCase):

	def setUp(self):
		self.runner = CliRunner()

	@mock_cloudformation
	def test_create_bastion(self):
		result = self.runner.invoke(
			cli,
			['create', 'test-stack', 
			'--availability-zone=sa-east-1a',
			'--key-pair-name=qa-vpc',
			'--subnet-id=subnet-0c5e5c68',
			'--region-name=sa-east-1'
		])

		self.assertEqual(result.exit_code, 0)
		self.assertEqual(result.output, 'bastion created.\n')
