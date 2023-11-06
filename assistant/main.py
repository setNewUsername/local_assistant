# import logger
from core.modules.logger.logger.Logger import logger
# import logger

# import path resolver
from core.modules.path_resolver.PathResolver.PathResolver import PathResolver
# import path resolver

from core.modules.logger.logFilesEnum import LogFiles

from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile
from core.modules.logger.logFuncs import logMethodToConsole

# init path resolver
pathResolver = PathResolver()
# init path resolver

# init logger
logger.setCommonLogDirPath(pathResolver.getLogsPath())
print(logger.logDirPath)
print(logger.checkLogFolderState())
logger.setupCommonLogFile()
logger.registerLogFile(LogFiles.TEST_LOG_FILE)
# init logger


class TestClass(LogClient):

    def __init__(self, logFile) -> None:
        super().__init__(logFile)

    @logMethodToFile('hello log to file')
    def testMethodToFile(self, phrase):
        print(phrase)

    @logMethodToConsole('hello log to console')
    def testMethodToConsole(self, phrase):
        print(phrase)


tst = TestClass(LogFiles.COMMON_LOG_FILE)

tst.testMethodToFile('hello')
tst.testMethodToConsole('hello')

logger.unregisterLogFiles()
logger.closeCommonLogFile()
