# coding: utf-8

from __future__ import (
    absolute_import,
    unicode_literals
)

from boto.cloudformation.connection import CloudFormationConnection
from boto.vpc import VPCConnection
from boto.regioninfo import _get_region


class ConnectionManager(object):
    """
    A handler of multi connections to AWS.
    """

    def __init__(self, aws_access_key_id,
                 aws_secret_access_key, region_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self._vpc_connection = None
        self._cloudformation_connection = None

    @property
    def vpc(self):
        if not self._vpc_connection:
            self._vpc_connection = VPCConnection(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region=self.region
            )
        return self._vpc_connection

    @property
    def cloudformation(self):
        if not self._cloudformation_connection:
            region = _get_region('cloudformation', self.region_name)

            self._cloudformation_connection = CloudFormationConnection(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region=region
            )
        return self._cloudformation_connection
