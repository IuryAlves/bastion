# coding: utf-8

import time
from boto.cloudformation.connection import CloudFormationConnection
from boto.regioninfo import _get_region
from boto.exception import BotoServerError
from .events_colors import event_color_map


class Bastion(object):

    def __init__(self, template,
                 region_name,
                 availability_zone,
                 key_name, subnet_id,
                 instance_name=None,
                 stack_name=None,
                 aws_access_key_id=None,
                 aws_secret_access_key=None,
                 iam_instance_profile=None,
                 image_id='ami-37cfad5b',
                 instance_type='t2.micro',
                 security_groups_ids=None):

        self.template = template
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.availability_zone = availability_zone
        self.key_name = key_name
        self.subnet_id = subnet_id
        self.iam_instance_profile = iam_instance_profile
        self.image_id = image_id
        self.instance_type = instance_type
        self.security_groups_ids = security_groups_ids
        self.region_name = region_name
        self.region = _get_region('cloudformation', self.region_name)
        self.stack_name = stack_name
        self.instance_name = instance_name

        if self.stack_name is None:
            self.stack_name = 'bastion-{availability_zone}-{subnet_id}'.format(
                availability_zone=self.availability_zone,
                subnet_id=self.subnet_id)

        if self.instance_name is None:
            self.instance_name = self.stack_name

        self.connection = CloudFormationConnection(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region=self.region
        )

    def create(self):
        parameters = [
            ('AvailabilityZone', self.availability_zone),
            ('ImageId', self.image_id),
            ('InstanceType', self.instance_type),
            ('KeyName', self.key_name),
            ('SubnetId', self.subnet_id),
            ('InstanceName', self.instance_name)
        ]

        if self.iam_instance_profile is not None:
            parameters.append(
                ('IamInstanceProfile', self.iam_instance_profile),
            )

        if self.security_groups_ids is not None:
            parameters.append(
                ('SecurityGroupIds', self.security_groups_ids),
            )

        self.connection.create_stack(
            self.stack_name,
            template_body=self.template,
            parameters=parameters
        )

    def delete(self):
        self.connection.delete_stack(self.stack_name)

    def events(self):
        _events_ids = []
        while True:
            try:
                for event in self.connection.describe_stack_events(self.stack_name):
                    if event.event_id not in _events_ids:
                        color = event_color_map.get(event.resource_status, '')
                        print('{0}{1}'.format(color, event))

                        _events_ids.append(event.event_id)
                time.sleep(1)

            except (BotoServerError, KeyboardInterrupt):
                break