from enum import Enum


class LogFiles(Enum):
    COMMON_LOG_FILE = 'main_log.log'
    TEST_LOG_FILE = 'test_log.log'
    CONFIGURATION_LOG_FILE = 'config_log.log'
    DOMAIN_CONTROLLER_LOG_FILE = 'dom_cntr_log.log'
    COMMANDS_CONTROLLER_LOG_FILE = 'com_cntr_log.log'
    SPEECH_CONTROLLER_LOG_FILE = 'speech_log.log'
    UTILS_LOG_FILE = 'utils_log.log'
