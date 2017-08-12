# coding: utf-8

import unittest
import mock
from moto import mock_cloudformation, mock_ec2
from bastion import read_template, Bastion


class AWSProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.template = read_template('aws', 'bastion.json')
        self.mock_availability_zone = mock.patch(
            'bastion.providers.aws.bastion.Bastion.discover_availability_zone'
        ).start()
        self.mock_availability_zone.return_value = 'sa-east-1a'

    def tearDown(self):
        mock.patch.stopall()

    @mock_cloudformation
    @mock_ec2
    def test_create_bastion(self):

        bastion = Bastion(
            self.template,
            'sa-east-1a',
            'ssh-key',
            'subnet-i233',
        )
        bastion.create()

        self.assertEqual(bastion.instance_name, bastion.stack_name)
        self.assertEqual(bastion.availability_zone, 'sa-east-1a')

    @mock_cloudformation
    @mock_ec2
    def test_create_bastion_stack_status_is_create_complete(self):

        bastion = Bastion(
            self.template,
            'sa-east-1a',
            'ssh-key',
            'subnet-i233'
        )
        bastion.create()
        stack = bastion.connection_manager.cloudformation.describe_stacks(
            bastion.stack_name)[0]

        self.assertEqual(stack.stack_status, 'CREATE_COMPLETE')


if __name__ == '__main__':
    unittest.main()
