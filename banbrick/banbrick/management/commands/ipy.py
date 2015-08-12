#!/usr/bin/env python
# encoding: utf-8

from ycyc.base.shelltools import ShellCommands
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'update the database models'

    def handle(self, *args, **options):
        return ShellCommands.ipython.check_call()
