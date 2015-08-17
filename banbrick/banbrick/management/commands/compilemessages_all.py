#!/usr/bin/env python
# encoding: utf-8

import os
import signal
import sys

from ycyc.base.filetools import cd, PathInfo
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'compile messages for all custom applications'

    def handle(self, *args, **options):
        locale_paths = set(getattr(settings, "LOCALE_PATHS", ()))
        base_dir = getattr(settings, "BASE_DIR", os.getcwd())
        for app in getattr(settings, "INSTALLED_APPS", ()):
            app_path = os.path.join(base_dir, app)
            if os.path.isdir(app_path):
                cwd_names = set(os.listdir(app_path))
                if not cwd_names & locale_paths:
                    continue
                with cd(app_path):
                    execute_from_command_line(["lyc", "compilemessages"])
