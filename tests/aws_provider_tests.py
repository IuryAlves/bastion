# coding: utf-8

import unittest
from moto import mock_cloudformation
from bastion import read_template, Bastion


class AWSProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.template = read_template('aws', 'bastion.json')

    @mock_cloudformation
    def test_create_bastion(self):

        bastion = Bastion(
            self.template,
            'sa-east-1a',
            'ssh-key',
            'subnet-i233'
        )
        bastion.create()
        stacks = bastion.connection.describe_stacks(bastion.stack_name)

        self.assertEqual(
            bastion.stack_name,
            'bastion-{0}-{1}'.format(
                bastion.availability_zone,
                bastion.subnet_id
            ))
        self.assertEqual(bastion.instance_name, bastion.stack_name)
        self.assertEqual(bastion.region, None)
        self.assertEqual(len(stacks), 1)

    @mock_cloudformation
    def test_create_bastion_stack_status_is_create_complete(self):

        bastion = Bastion(
            self.template,
            'sa-east-1a',
            'ssh-key',
            'subnet-i233'
        )
        bastion.create()
        stack = bastion.connection.describe_stacks(bastion.stack_name)[0]

        self.assertEqual(stack.stack_status, 'CREATE_COMPLETE')

    @mock_cloudformation
    def test_create_bastion_get_region_by_name(self):
        bastion = Bastion(
            self.template,
            'sa-east-1a',
            'ssh-key',
            'subnet-123',
            region_name='sa-east-1'
        )

        self.assertEqual(bastion.region.name, 'sa-east-1')


if __name__ == '__main__':
    unittest.main()
