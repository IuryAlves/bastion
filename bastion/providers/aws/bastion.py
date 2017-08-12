# coding: utf-8

from __future__ import (
    unicode_literals,
    absolute_import
)


from .connection_manager import ConnectionManager


class Bastion(object):

    def __init__(self, template,
                 availability_zone,
                 key_pair_name, subnet_id,
                 region_name=None,
                 instance_name=None,
                 stack_name=None,
                 aws_access_key_id=None,
                 aws_secret_access_key=None,
                 image_id='ami-37cfad5b',
                 instance_type='t2.micro',
                 security_groups_ids=None,
                 connection_manager_class=None):

        self.template = template
        self.availability_zone = availability_zone
        self.key_pair_name = key_pair_name
        self.subnet_id = subnet_id
        self.image_id = image_id
        self.instance_type = instance_type
        self.security_groups_ids = security_groups_ids
        self.region_name = region_name
        self.stack_name = stack_name
        self.instance_name = instance_name

        self._connection_manager_class = connection_manager_class or ConnectionManager
        self.connection_manager = self._connection_manager_class(
            aws_access_key_id,
            aws_secret_access_key,
            self.region_name)

        if self.stack_name is None:
            self.stack_name = 'bastion-{availability_zone}-{subnet_id}'.format(
                availability_zone=self.availability_zone,
                subnet_id=self.subnet_id)

        if self.instance_name is None:
            self.instance_name = self.stack_name

    def create(self):
        parameters = [
            ('AvailabilityZone', self.availability_zone),
            ('ImageId', self.image_id),
            ('InstanceType', self.instance_type),
            ('KeyPairName', self.key_pair_name),
            ('SubnetId', self.subnet_id),
            ('InstanceName', self.instance_name)
        ]

        if self.security_groups_ids is not None:
            parameters.append(
                ('SecurityGroupIds', self.security_groups_ids),
            )

        self.connection_manager.cloudformation.create_stack(
            self.stack_name,
            template_body=self.template,
            parameters=parameters
        )

    def delete(self):
        self.connection_manager.cloudformation.delete_stack(self.stack_name)

    def check_status(self, status):
        for event in self.connection_manager.cloudformation.describe_stack_events(self.stack_name):
            if event.resource_status == 'CREATE_COMPLETE':
                return True
        return False

    def discover_availability_zone(self):
        raise NotImplementedError
        # subnets = self.connection_manager.vpc_connection.get_all_subnets(
        #     subnet_ids=[self.subnet_id]
        # )
        # return subnets[0].availability_zone
