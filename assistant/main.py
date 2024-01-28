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

# models imports
import core.models.sp_domains_models as dom
import core.models.commands_models as com
import core.models.configuration as conf
# models imports

from core.modules.databaseConnectionRunner.dbConnRunner import dbConnRunnerPGSQL
from core.modules.modelsController.modelsController import ModelsController

from core.modules.modelsController.viewsController import ViewsController

proc15 = 65535 * 0.15

# init path resolver
pathResolver = PathResolver()
# init path resolver

# init logger
logger.setCommonLogDirPath(pathResolver.getLogsPath())
logger.setupCommonLogFile()
# init logger

# init connection to DB
dbconn = dbConnRunnerPGSQL(LogFiles.DB_CONN_RUNNER, pathResolver.getDBDataStoragePath(), 'postgre_sql_connect.json')
conn = dbconn.connectToDb()
# init connection to DB

# init DB views controller
vcon = ViewsController(conn, pathResolver.getSQLCreateViewsDir(), LogFiles.DB_VIEW_CONTROLLER)
# init DB views controller

# init config controller
confCont = ConfigController('config.json',
                            pathResolver.getConfigsPath(),
                            LogFiles.CONFIGURATION_LOG_FILE)
if not confCont.checkConfigFile():
    confCont.recreateConfigFile()
confCont.setDefaultConfigIfEmpty()
confCont.readDataFromConfigFile()
# init config controller

# init models controller
mw = ModelsController(LogFiles.MODELS_CONTROLLER, confCont, vcon)
# init models controller

# create commands tables
mw.createTables([com.CommandType, com.CommandTypesFields, com.CommandFieldsData, com.Command, com.CommandsData], conn)
mw.createTables([dom.Domain, dom.DomainsRel], conn)
mw.createTables([conf.Configuration], conn)
# create commands tables
# create views
vcon.createViewFromSQLFiles()
# create views

# mw.transferFromJSONtoDB(conn)
dbConfigData = mw.transferFromDBtoJSON()
confCont.setConfigDataToDBConfig(dbConfigData)

# init domains controller
domCntr = SpeechDomainsController(LogFiles.DOMAIN_CONTROLLER_LOG_FILE)
domCntr.addDomains(confCont.getDomainsData())
# confCont.updateDomainsData(domCntr.serializeDomains())
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
    LogFiles.UTILS_LOG_FILE,
    pathResolver.getGrammarFileDir(),
    confCont.getGrammarFile(),
    domCntr.rootDomain
)

gramGen.rebuild()

spCntr.setDictFile(confCont.getDictFile())
spCntr.setGrammarFile(confCont.getGrammarFile())
spCntr.setModelFiles(confCont.getModelFiles())
spCntr.setLang(confCont.getLanguageModel())

spCntr.startListening()

dbconn.disconnect()
logger.unregisterLogFiles()
logger.closeCommonLogFile()
