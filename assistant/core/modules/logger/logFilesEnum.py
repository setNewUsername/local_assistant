from enum import Enum


class LogFiles(Enum):
    COMMON_LOG_FILE = 'main_log.log'
    TEST_LOG_FILE = 'test_log.log'
    CONFIGURATION_LOG_FILE = 'config_log.log'
    DOMAIN_CONTROLLER_LOG_FILE = 'dom_cntr_log.log'
