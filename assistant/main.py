# import logger
from core.modules.logger.logger.Logger import logger
# import logger

# import path resolver
from core.modules.path_resolver.PathResolver.PathResolver import PathResolver
# import path resolver

from core.modules.logger.logFilesEnum import LogFiles

from core.modules.configurationController.configurationController.configurationController import ConfigController

from core.modules.domainController.domainController.domainController import SpeechDomainsController

from core.modules.commandsController.commands.callProgrammCommand import CallProgrammCommand
from core.modules.commandsController.commands.systemCommand import SysCommand

from core.modules.commandsController.commands.commandsEnum import CommandTypes

from core.modules.commandsController.commandsController.commandsController import CommandController

# init path resolver
pathResolver = PathResolver()
# init path resolver

# init logger
logger.setCommonLogDirPath(pathResolver.getLogsPath())
print(logger.logDirPath)
print(logger.checkLogFolderState())
logger.setupCommonLogFile()
logger.registerLogFile(LogFiles.TEST_LOG_FILE)
logger.registerLogFile(LogFiles.CONFIGURATION_LOG_FILE)
logger.registerLogFile(LogFiles.DOMAIN_CONTROLLER_LOG_FILE)
logger.registerLogFile(LogFiles.COMMANDS_CONTROLLER_LOG_FILE)
# init logger

# init config controller
confCont = ConfigController('config.json',
                            pathResolver.getConfigsPath(),
                            LogFiles.CONFIGURATION_LOG_FILE)
if not confCont.checkConfigFile():
    confCont.recreateConfigFile()
confCont.setDefaultConfigIfEmpty()
# init config controller

# init domains controller
domCntr = SpeechDomainsController(LogFiles.DOMAIN_CONTROLLER_LOG_FILE)
testDomain = {
    'domain_word': 'test',
    'parent_dom_uuid': '111',
    'domain_uuid': '111',
    'command_uuid': 'none'
}
testDomain0 = {
    'domain_word': 'test0',
    'parent_dom_uuid': '111',
    'domain_uuid': '110',
    'command_uuid': 'none'
}
testDomain1 = {
    'domain_word': 'test1',
    'parent_dom_uuid': '111',
    'domain_uuid': '112',
    'command_uuid': 'none'
}
testDomain11 = {
    'domain_word': 'test11',
    'parent_dom_uuid': '112',
    'domain_uuid': '113',
    'command_uuid': 'none'
}
testDomain12 = {
    'domain_word': 'test12',
    'parent_dom_uuid': '112',
    'domain_uuid': '114',
    'command_uuid': 'none'
}
domCntr.setRootDomain(testDomain)
domCntr.addDomain(testDomain1)
domCntr.addDomain(testDomain11)
domCntr.addDomain(testDomain12)
domCntr.addDomain(testDomain0)
# print(domCntr.findDomainCommandBySpeechStr('test_test0'))
# init domains controller

# init command controller

cmdCtrl = CommandController(LogFiles.COMMANDS_CONTROLLER_LOG_FILE)

cmd1 = {
    'uuid': 'id1',
    'type': 'call_prog',
    'prog_path': 'notepad.exe',
    'prog_args': ['C:\\Users\\ANDMASL\\Desktop\\test.txt']
}

cmd2 = {
    'uuid': 'id2',
    'type': 'sys_command',
    'sys_command': 'del /f C:\\Users\\ANDMASL\\Desktop\\test.txt'
}

cmdCtrl.addCommand(cmd1)
cmdCtrl.addCommand(cmd2)

# cmdCtrl.callCommandByUuid('id1')
# cmdCtrl.callCommandByUuid('id2')

confCont.updateDomainsData(domCntr.serializeDomains())
confCont.updateCommandsData(cmdCtrl.serializeCommands())

confCont.writeDataToConfigFile()

# init command controller

logger.unregisterLogFiles()
logger.closeCommonLogFile()
