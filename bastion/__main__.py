# coding: utf-8

import click
from . import create_bastion
from .providers.aws import defaults


click.disable_unicode_literals_warnings = True


@click.group()
def cli():
    """
    Easily create and manage bastion hosts
    """
    pass


@cli.command()
@click.argument('stack-name')
@click.option('--availability-zone', help='The Availability Zone where bastion will be launched')
@click.option('--key-pair-name', help='The Key Pair Name used to access the bastion ')
@click.option('--subnet-id', help='The subnet-id where bastion will be launched. Should be a public subnet')
@click.option('--region-name', help='The AWS Region where the bastion will be launched')
@click.option('--instance-name', help='The name of the bastion. The default is the same of stack-name')
@click.option('--aws-access-key-id')
@click.option('--aws-secret-access-key')
@click.option('--image-id', help='The AWS AMI that will be used in bastion', default=defaults.DEFAULT_AMI)
@click.option('--instance-type', help='The instance type of the bastion', default=defaults.DEFAULT_INSTANCE_TYPE)
@click.option('--security-groups-ids', help='A list of security groups ids to allow traffic to the bastion')
@click.pass_context
def create(ctx, stack_name, availability_zone, key_pair_name,
           subnet_id, region_name, instance_name,
           aws_access_key_id, aws_secret_access_key,
           image_id, instance_type, security_groups_ids):

    if not all([availability_zone, key_pair_name, subnet_id]):
        raise click.UsageError(
            'You must pass at least --availability-zone, --key-pair-name and '
            '--subnet-id'
        )

    click.secho(
        'Creating Bastion host with the following properties:\n', fg='green')
    for param in ctx.params.items():
        if param[1]:
            click.secho('{0}: {1}'.format(*param))

    try:
        create_bastion(
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
    except Exception as e:
        click.secho('Bastion failed to create.', fg='red')
        click.secho(e, fg='red')
    else:
        click.secho('Bastion created.', fg='green')


if __name__ == '__main__':
    cli()
