"""PyYAML fix

Disable resolving of Off/On/Yes/No
in YAML 1.2 (which in 2009 superseded the 1.1 specification from 2005) this usage of Off/On/Yes/No was dropped

It has not been implemented yet: https://github.com/yaml/pyyaml/issues/116

https://stackoverflow.com/questions/36463531/pyyaml-automatically-converting-certain-keys-to-boolean-values

Usage:

    with open(yaml_fpath, 'r') as stream:
        try:
            return yaml.load(stream, CustomSafeLoader) # eliminates resolving of Off/On/Yes/No
            # return yaml.safe_load(stream)

There is an alternative: YAML 1.2 loader - ruamel.yam, but it seems broken

"""
 
__author__ = "Ivan Abramov"
__maintainer__ = "Ivan Abramov"

from yaml.reader import *
from yaml.scanner import *
from yaml.parser import *
from yaml.composer import *
from yaml.resolver import *

from yaml.constructor import SafeConstructor

# Create custom safe constructor class that inherits from SafeConstructor
class SustomSafeConstructor(SafeConstructor):

    bool_values = {
            'yes':      'yes',
            'no':       'no',
            'true':     True,
            'false':    False,
            'on':       'on',
            'off':      'off',
        }

class CustomSafeLoader(Reader, Scanner, Parser, Composer, SustomSafeConstructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SustomSafeConstructor.__init__(self)
        Resolver.__init__(self)