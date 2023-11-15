# import logger
from core.modules.logger.logger.Logger import logger
# import logger

# import path resolver
from core.modules.path_resolver.PathResolver.PathResolver import PathResolver
# import path resolver

from core.modules.logger.logFilesEnum import LogFiles

from core.modules.configurationController.configurationController.configurationController import ConfigController

from core.modules.domainController.domainController.domainController import SpeechDomainsController

from core.modules.commandsController.commandsController.commandsController import CommandController

from core.modules.speechController.speechPreprocessor.speechPreprocessor import SpeechPreprocessor

from core.modules.speechController.speechController.speechController import SpeechController

from core.modules.utils.text2dictUtil import Text2DictUtil
from core.modules.utils.grammarGenerator import GarammarGenerator

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
domains = [
    {'domain_word': 'компьютер',
     'parent_dom_uuid': 'none',
     'domain_uuid': '110',
     'command_uuid': 'none'
     },
    {'domain_word': 'скажи',
     'parent_dom_uuid': '110',
     'domain_uuid': '111',
     'command_uuid': 'none'
    },
    {'domain_word': 'привет',
     'parent_dom_uuid': '111',
     'domain_uuid': '112',
     'command_uuid': 'none'
    },
    {'domain_word': 'пока',
     'parent_dom_uuid': '111',
     'domain_uuid': '113',
     'command_uuid': 'none'
    },
    {'domain_word': 'как дела',
     'parent_dom_uuid': '111',
     'domain_uuid': '114',
     'command_uuid': 'none'
    },
]
domCntr = SpeechDomainsController(LogFiles.DOMAIN_CONTROLLER_LOG_FILE)
print(confCont.getDomainsData())
domCntr.addDomains(domains)
# init domains controller

# init command controller
cmdCtrl = CommandController(LogFiles.COMMANDS_CONTROLLER_LOG_FILE)
cmdCtrl.addCommands(confCont.getComandsData())
# init command controller

# init speech preprocessor
spPrep = SpeechPreprocessor(domCntr.getDomainsBatches())
# init speech preprocessor

spCntr = SpeechController(
    LogFiles.SPEECH_CONTROLLER_LOG_FILE,
    spPrep,
    domCntr,
    cmdCtrl
)

t2dU = Text2DictUtil(
    LogFiles.UTILS_LOG_FILE,
    'D:\\projects\\local_assistant\\3d_party\\ru4sphinx\\text2dict\\dict2transcript.pl',
    pathResolver.getLocalDataStoragePath(),
    pathResolver.getModelDictDir(),
    confCont.getDictFile()
)

t2dU.setWordList(domCntr.getWordList())

t2dU.setUp()
t2dU.translate()

gramGen = GarammarGenerator(
    pathResolver.getGrammarFileDir(),
    confCont.getGrammarFile(),
    domCntr.rootDomain
)

# print(gramGen.batchesLineBuffer)
gramGen.rebuild()

spCntr.setDictFile(confCont.getDictFile())
spCntr.setGrammarFile(confCont.getGrammarFile())
spCntr.setModelFiles(confCont.getModelFiles())
spCntr.setLang(confCont.getLanguageModel())

spCntr.startListening()

logger.unregisterLogFiles()
logger.closeCommonLogFile()
