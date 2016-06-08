#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright 2016 Sean "Shaleh" Perry

DOCUMENTATION = '''
---
module: read_ini
short_description: Read settings in INI files
description:
     - Read individual settings in an INI-style file
version_added: "0.9"
options:
  path:
    description:
      - Path to the INI-style file
    required: true
    default: null
  section:
    description:
      - Section name in INI file.
    required: true
    default: null
  option:
    description:
      - Name of the option to read.
    required: true
    default: null
requirements: [ ConfigParser ]
author: Sean "Shaleh" Perry
'''

EXAMPLES = '''
# Read "fav" from section "[drinks]" in specified file.
- read_ini: path=/etc/conf section=drinks option=fav
'''

import ConfigParser
import sys

from ansible.module_utils.basic import *


class ReadIniException(Exception):
    pass


def do_read_ini(module, filename, section=None, option=None):
    cp = ConfigParser.ConfigParser()
    cp.optionxform = lambda x: x  # identity function to prevent casting

    try:
        with open(filename) as fp:
            cp.readfp(fp)
    except IOError as e:
        raise ReadIniException("failed to read {}: {}".format(filename, e))

    try:
        return cp.get(section, option)
    except ConfigParser.NoSectionError:
        raise ReadIniException("section does not exist: " + section)
    except ConfigParser.NoOptionError:
        raise ReadIniException("option does not exist: " + option)


def main():
    spec = {
        'path': {'required': True},
        'section': {'required': True},
        'option': {'required': True},
    }
    module = AnsibleModule(argument_spec=spec)

    path = os.path.expanduser(module.params['path'])
    section = module.params['section']
    option = module.params['option']

    try:
        value = do_read_ini(module, path, section, option)
        module.exit_json(path=path, changed=True, value=value)
    except ReadIniException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
