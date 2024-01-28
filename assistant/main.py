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

proc15 = 65535 * 0.15

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
    {
        'domain_word': 'компьютер',
        'parent_dom_uuid': 'none',
        'domain_uuid': '110',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'запусти',
        'parent_dom_uuid': '110',
        'domain_uuid': '115',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'дота два',
        'parent_dom_uuid': '115',
        'domain_uuid': '130',
        'command_uuid': 'id9'
    },
    {
        'domain_word': 'блокнот',
        'parent_dom_uuid': '115',
        'domain_uuid': '116',
        'command_uuid': 'id1'
    },
    {
        'domain_word': 'аниме',
        'parent_dom_uuid': '115',
        'domain_uuid': '117',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'Сага о винленде',
        'parent_dom_uuid': '117',
        'domain_uuid': '118',
        'command_uuid': 'id2'
    },
    {
        'domain_word': 'убавь',
        'parent_dom_uuid': '110',
        'domain_uuid': '123',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'звук на пятнадцать процентов',
        'parent_dom_uuid': '123',
        'domain_uuid': '125',
        'command_uuid': 'id5'
    },
    {
        'domain_word': 'прибавь',
        'parent_dom_uuid': '110',
        'domain_uuid': '124',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'звук на пятнадцать процентов',
        'parent_dom_uuid': '124',
        'domain_uuid': '126',
        'command_uuid': 'id6'
    },
    {
        'domain_word': 'выключи',
        'parent_dom_uuid': '110',
        'domain_uuid': '119',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'звук',
        'parent_dom_uuid': '119',
        'domain_uuid': '121',
        'command_uuid': 'id3'
    },
    {
        'domain_word': 'включи',
        'parent_dom_uuid': '110',
        'domain_uuid': '120',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'звук',
        'parent_dom_uuid': '120',
        'domain_uuid': '122',
        'command_uuid': 'id4'
    },
    {
        'domain_word': 'переключи звук на',
        'parent_dom_uuid': '110',
        'domain_uuid': '127',
        'command_uuid': 'none'
    },
    {
        'domain_word': 'динамики',
        'parent_dom_uuid': '127',
        'domain_uuid': '128',
        'command_uuid': 'id8'
    },
    {
        'domain_word': 'наушники',
        'parent_dom_uuid': '127',
        'domain_uuid': '129',
        'command_uuid': 'id7'
    },
]
# domCntr = SpeechDomainsController(LogFiles.DOMAIN_CONTROLLER_LOG_FILE)
# print(confCont.getDomainsData())
# domCntr.addDomains(domains)
# confCont.updateDomainsData(domCntr.serializeDomains())
# print(confCont.getDomainsData())
# # init domains controller

commands = [
    {
        'uuid': 'id1',
        'type': 'call_prog',
        'prog_path': 'notepad.exe',
        'prog_args': ['C:\\Users\\ANDMASL\\Desktop\\test.txt']
    },
    {
        'uuid': 'id2',
        'type': 'sys_command',
        'sys_command': 'start chrome https://jut.su/vinland-saga/'
    },
    {
        'uuid': 'id3',
        'type': 'sys_command',
        'sys_command': 'D:\\projects\\local_assistant\\assistant\\core\\system_utils\\media_control\\nircmd.exe mutesysvolume 1' # mute
    },
    {
        'uuid': 'id4',
        'type': 'sys_command',
        'sys_command': 'D:\\projects\\local_assistant\\assistant\\core\\system_utils\\media_control\\nircmd.exe mutesysvolume 0' # unmute
    },
    {
        'uuid': 'id5',
        'type': 'sys_command',
        'sys_command': f'D:\\projects\\local_assistant\\assistant\\core\\system_utils\\media_control\\nircmd.exe changesysvolume -{proc15}' # decrease by 15%
    },
    {
        'uuid': 'id6',
        'type': 'sys_command',
        'sys_command': f'D:\\projects\\local_assistant\\assistant\\core\\system_utils\\media_control\\nircmd.exe changesysvolume {proc15}' # increase by 15%
    },
    {
        'uuid': 'id7',
        'type': 'sys_command',
        'sys_command': 'D:\\projects\\local_assistant\\assistant\\core\\system_utils\\media_control\\nircmd.exe setdefaultsounddevice "Динамики"' # headphones
    },
    {
        'uuid': 'id8',
        'type': 'sys_command',
        'sys_command': 'D:\\projects\\local_assistant\\assistant\\core\\system_utils\\media_control\\nircmd.exe setdefaultsounddevice "5 - XV240Y P"' # monitor sound
    },
    {
        'uuid': 'id9',
        'type': 'call_prog',
        'prog_path': 'H:\\SteamLibrary\\steamapps\\common\\dota 2 beta\\game\\bin\\win64\\dota2.exe',
        'prog_args': []
    }
]

# # init command controller
# cmdCtrl = CommandController(LogFiles.COMMANDS_CONTROLLER_LOG_FILE)
# print(confCont.getComandsData())
# cmdCtrl.addCommands(commands)
# # init command controller

# # init speech preprocessor
# spPrep = SpeechPreprocessor(domCntr.getDomainsBatches())
# # init speech preprocessor

# spCntr = SpeechController(
#     LogFiles.SPEECH_CONTROLLER_LOG_FILE,
#     spPrep,
#     domCntr,
#     cmdCtrl
# )

# t2dU = Text2DictUtil(
#     LogFiles.UTILS_LOG_FILE,
#     'D:\\projects\\local_assistant\\3d_party\\ru4sphinx\\text2dict\\dict2transcript.pl',
#     pathResolver.getLocalDataStoragePath(),
#     pathResolver.getModelDictDir(),
#     confCont.getDictFile()
# )

# t2dU.setWordList(domCntr.getWordList())

# t2dU.setUp()
# t2dU.translate()

# gramGen = GarammarGenerator(
#     LogFiles.UTILS_LOG_FILE,
#     pathResolver.getGrammarFileDir(),
#     confCont.getGrammarFile(),
#     domCntr.rootDomain
# )

# gramGen.rebuild()

# spCntr.setDictFile(confCont.getDictFile())
# spCntr.setGrammarFile(confCont.getGrammarFile())
# spCntr.setModelFiles(confCont.getModelFiles())
# spCntr.setLang(confCont.getLanguageModel())

# spCntr.startListening()

from peewee import *
import core.models.sp_domains_models as dom
import core.models.commands_models as com
import core.models.configuration as conf

from core.modules.logger.logFilesEnum import LogFiles
from core.modules.databaseConnectionRunner.dbConnRunner import dbConnRunnerPGSQL
from core.modules.modelsController.modelsController import ModelsController

from core.modules.modelsController.viewsController import ViewsController
from core.modules.modelsController.viewsController import DBViewEnum

dbconn = dbConnRunnerPGSQL(LogFiles.DB_CONN_RUNNER, pathResolver.getDBDataStoragePath(), 'postgre_sql_connect.json')
conn = dbconn.connectToDb()

vcon = ViewsController(conn, pathResolver.getSQLCreateViewsDir(), LogFiles.DB_VIEW_CONTROLLER)
mw = ModelsController(LogFiles.MODELS_CONTROLLER, confCont, vcon)
# create commands tables
mw.createTables([com.CommandType, com.CommandTypesFields, com.CommandFieldsData, com.Command, com.CommandsData], conn)
mw.createTables([dom.Domain, dom.DomainsRel], conn)
mw.createTables([conf.Configuration], conn)
# create commands tables
# create views
vcon.createViewFromSQLFiles()
# create views

mw.transferFromJSONtoDB(conn)
print(mw.transferFromDBtoJSON())

dbconn.disconnect()
logger.unregisterLogFiles()
logger.closeCommonLogFile()
