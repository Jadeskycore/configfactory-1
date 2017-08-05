#!/usr/bin/env python
import os
import sys

from configfactory.support import dirs


if __name__ == "__main__":

    os.environ.setdefault("CONFIGFACTORY_CONFIG", dirs.root_dir('configfactory.dev.yml'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configfactory.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
