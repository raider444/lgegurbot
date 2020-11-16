'''An application context'''
 
__author__ = "Ivan Abramov"
__maintainer__ = "Ivan Abramov"

import os, yaml, configparser

import logging
log = logging.getLogger(__name__)

from .custom_safe_loader import CustomSafeLoader

class Context:
    """An application context class
    """
    tool_name = None
    cfg = None
    args = None
    base_path = None
    hr_width = None

    template_path = None

    def __init__(self, tool_name, args, base_path ):
        '''Initialises context

        :param str tool_name: the name of this tool
        :param dict args: cli argument parsed with the ArgumentParser
        :param str base_path: path to this tool folder 
        :param str hr_width: the width in characters of a horizontal divider
        '''
        self.tool_name = tool_name
        self.args = args
        self.base_path = base_path

        self.template_path = os.path.join(base_path, 'template') 
        self.cfg_path = os.path.join(base_path, 'conf') 

        # load the config file
        self.cfg = self.load_yaml(os.path.join(self.cfg_path, "config.yml"))

        # TODO
        # self.cfg = self.load_yaml(os.path.join('/etc', f"{self.tool_name}.yml"))

        if "settings" in self.cfg:
            settings = self.cfg['settings']
            if "hr_width" in settings:
                # Horizontal log delimiter
                self.hr_width = settings['hr_width']

        self.hr = '=' * self.hr_width


    def load_yaml(self, yaml_fpath):
        '''Reads yaml file
        YAML 1.2 support

        Disables resolving of Off/On/Yes/No
        in YAML 1.2 (which in 2009 superseded the 1.1 specification from 2005) this usage of Off/On/Yes/No was dropped

        It has not been implemented yet in PyYAML: https://github.com/yaml/pyyaml/issues/116

        https://stackoverflow.com/questions/36463531/pyyaml-automatically-converting-certain-keys-to-boolean-values

        :param str yaml_fpath: YAML file path
        '''

        log.info(f"Loading: {yaml_fpath}")

        with open(yaml_fpath, 'r') as stream:
            try:
                return yaml.load(stream, CustomSafeLoader) # eliminates resolving of Off/On/Yes/No
                # return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                log.exception(yaml_fpath)
                raise