#!/usr/bin/env python
# encoding: utf-8

import os
import signal
import sys

from ycyc.base.shelltools import ShellCommands
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'update the database models'

    def handle(self, *args, **options):
        ipython = ShellCommands.ipython()

        def signal_to_ipy(sig, s):
            os.kill(ipython.pid, sig)

        signal.signal(signal.SIGINT, signal_to_ipy)
        ipython.communicate()
        sys.exit(ipython.poll())
