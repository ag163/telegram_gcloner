#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import logging
import os
import shutil
import sys


logger = logging.getLogger(__name__)


class _Config:
    def __init__(self):
        self._ad_string = ''
        self._log_file = ''
        self._telegram_token = None
        self._path_to_gclone = None
        self._key_string_folder_id = ''
        self._key_string_message_id = ''
        self._user_ids = ''
        self._group_ids = ''
        self._base_path = os.path.dirname(os.path.dirname(__file__))

    def load_config(self):
        logger.debug('Loading config')

        try:
            config_file = configparser.ConfigParser(allow_no_value=True)
            config_file.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini'), encoding='utf-8')
        except IOError as err:
            logger.warning("Can't open the config file: ", err)
            input('Press enter to exit.')
            sys.exit(1)

        if not config_file.has_section('General'):
            logger.warning("Can't find General section in config.")
            input('Press enter to exit.')
            sys.exit(1)

        config_general = config_file['General']

        config_general_keywords_str = [
            'path_to_gclone',
            'telegram_token',
            'user_ids',
            'group_ids',
            'ad_string',
        ]

        self.get_config_from_section('str', config_general_keywords_str, config_general)

        self._user_ids = [int(item) for item in self._user_ids.split(',')]
        self._group_ids = [int(item) for item in self._group_ids.split(',')]

        if not os.path.isfile(self._path_to_gclone):
            self._path_to_gclone = shutil.which('gclone')
            if not self._path_to_gclone:
                logger.warning('gclone executable is not found.')
                input("Press Enter to continue...")
                sys.exit(0)
        logger.info('Found gclone: ' + self._path_to_gclone)

        if not self._telegram_token:
            logger.warning('telegram token is not provided.')
            input("Press Enter to continue...")
            sys.exit(0)
        logger.info('Found token: ' + self._telegram_token)

    def get_config_from_section(self, var_type, keywords, section):
        for item in keywords:
            if var_type == 'int':
                value = section.getint(item, 0)
            elif var_type == 'str':
                value = section.get(item, '')
            elif var_type == 'bool':
                value = section.getboolean(item, False)
            else:
                raise TypeError
            if not value and value is not False:
                logger.warning('{} is not provided.'.format(item))
                input("Press Enter to continue...")
                sys.exit(1)
            logger.info('Found {}: {}'.format(item, value))
            setattr(self, '_' + item, value)

    @property
    def PATH_TO_GCLONE(self):
        return self._path_to_gclone

    @property
    def TELEGRAM_TOKEN(self):
        return self._telegram_token

    @property
    def USER_IDS(self):
        return self._user_ids

    @property
    def AD_STRING(self):
        return self._ad_string

    @property
    def GROUP_IDS(self):
        return self._group_ids

    @property
    def BASE_PATH(self):
        return self._base_path

    @property
    def LOG_FILE(self):
        return self._log_file

    @LOG_FILE.setter
    def LOG_FILE(self, val):
        self._log_file = val


config = _Config()
