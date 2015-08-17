#!/usr/bin/env python
# encoding: utf-8

import os
import signal
import sys

from ycyc.base.filetools import cd, PathInfo
from ycyc.base.shelltools import Command as ShellCommand
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'compile messages for all custom applications'

    def handle(self, *args, **options):
        command = ShellCommand("django-admin")
        locale_paths = set(getattr(settings, "LOCALE_PATHS", ()))
        for app in getattr(settings, "INSTALLED_APPS", ()):
            if os.path.isdir(app):
                with cd(app):
                    cwd_names = set(os.listdir("."))
                    if not cwd_names & locale_paths:
                        continue
                    command.check_call("compilemessages")
