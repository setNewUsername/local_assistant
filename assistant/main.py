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

from core.modules.speechController.speechPreprocessor.speechPreprocessor import SpeechPreprocessor

# init path resolver
pathResolver = PathResolver()
# init path resolver

# init logger
logger.setCommonLogDirPath(pathResolver.getLogsPath())
logger.setupCommonLogFile()
# init logger

# init config controller
confCont = ConfigController('config.json',
                            pathResolver.getConfigsPath(),
                            LogFiles.CONFIGURATION_LOG_FILE)
if not confCont.checkConfigFile():
    confCont.recreateConfigFile()
confCont.setDefaultConfigIfEmpty()
confCont.readDataFromConfigFile()
# init config controller

# init domains controller
domCntr = SpeechDomainsController(LogFiles.DOMAIN_CONTROLLER_LOG_FILE)
domCntr.addDomains(confCont.getDomainsData())
# init domains controller

# init command controller
cmdCtrl = CommandController(LogFiles.COMMANDS_CONTROLLER_LOG_FILE)
cmdCtrl.addCommands(confCont.getComandsData())
# init command controller

# init speech preprocessor
spPrep = SpeechPreprocessor(domCntr.getDomainsBatches())
# init speech preprocessor

print(domCntr.findDomainCommandBySpeechStr(spPrep.processSpeech('test test1 testb testb')))

logger.unregisterLogFiles()
logger.closeCommonLogFile()
