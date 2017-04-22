# coding: utf-8

import click
from . import create_bastion

click.disable_unicode_literals_warnings = True


@click.group()
def cli():
	pass


@cli.command()
@click.argument('stack-name')
@click.option('--availability-zone', help='The Availability Zone where bastion will be launched')
@click.option('--key-pair-name', help='The Key Pair Name used to access the bastion ')
@click.option('--subnet-id', help='The subnet-id where bastion will be launched. Should be a public subnet')
@click.option('--region-name', help='The AWS Region where the bastion will be launched')
@click.option('--instance-name', help='The name of the bastion. The default is the same of stack-name')
@click.option('--aws-access-key-id', help='')
@click.option('--aws-secret-access-key')
@click.option('--image-id', help='The AWS Ami that will be used in bastion', default='ami-37cfad5b')
@click.option('--instance-type', help='The instance type', default='t2.micro')
@click.option('--security-groups-ids', help='A list of security groups ids to allow traffic to the bastion')
def create(stack_name, availability_zone, key_pair_name,
				 subnet_id, region_name, instance_name,
				 aws_access_key_id, aws_secret_access_key,
				 image_id, instance_type, security_groups_ids):
	"""
	Easily create and manage bastion hosts in AWS VPCs
	"""
	if not any([availability_zone, key_pair_name, subnet_id]):
		raise click.UsageError(
			'You must pass at least availability_zone, key_pair_name and'
			'subnet_id'
		)
	bastion = create_bastion(
		availability_zone=availability_zone,
		key_pair_name=key_pair_name,
		subnet_id=subnet_id,
		region_name=region_name,
		instance_name=instance_name,
		stack_name=stack_name,
		aws_access_key_id=aws_access_key_id,
		aws_secret_access_key=aws_secret_access_key,
		image_id=image_id,
		instance_type=instance_type,
		security_groups_ids=security_groups_ids
	)

	click.echo('bastion created.')


if __name__ == '__main__':
	cli()
