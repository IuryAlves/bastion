# coding: utf-8

from __future__ import (
    unicode_literals,
    absolute_import
)

from os import path
from .providers.aws import Bastion


DIR_PATH = path.dirname(path.realpath(__file__))


def create_bastion(provider='aws', template_name='bastion.json', **kwargs):
    template = read_template(provider, template_name)
    bastion = Bastion(template, **kwargs)
    bastion.create()
    return bastion


def read_template(provider, template_name):
    template_path = path.join(DIR_PATH, 'providers',
                              provider, 'templates', template_name)
    with open(template_path) as template:
        return template.read()
