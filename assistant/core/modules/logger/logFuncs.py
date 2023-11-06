from core.modules.logger.logger.Logger import logger
from core.modules.logger.logFilesEnum import LogFiles


# class used to store logFile name and methods for method.__str__() transform
class LogClient:
    logFile: LogFiles = LogFiles.COMMON_LOG_FILE

    def __init__(self, lgFile) -> None:
        self.logFile = lgFile

    # returns caller from method.__str__()
    # example: <function TestClass.testMethod at 0x0000021B65D5E340>
    # returns: TestClass
    def getCaller(self, methodStr: str) -> str:
        return methodStr.split(' ')[1].split('.')[0]
    # returns caller from method.__str__()

    # return method name from method.__str__()
    # example: <function TestClass.testMethod at 0x0000021B65D5E340>
    # returns: testMethod
    def getMethodName(self, methodStr: str) -> str:
        return methodStr.split(' ')[1].split('.')[1]
    # return method name from method.__str__()
# class used to store logFile name and methods for method.__str__() transform


# decorator for method logging to log file
# example:
# @logMethodToFile('method called')
# def method(self, phrase)
#
# class.method('hello')
#
# result:
# class.testMethod(('hello',), {}) 17:59:32 - method called
def logMethodToFile(logText):
    def funcWrapper(function):
        def funcCall(self, *args, **kwargs):
            funcName = self.getMethodName(function.__str__())
            logger.logToLogFile(self.logFile,
                                logText,
                                coller=self.getCaller(function.__str__()),
                                functionName=funcName,
                                args=args,
                                kwargs=kwargs)
            return function(self, *args, **kwargs)
        return funcCall
    return funcWrapper
# decorator for method logging to log file


# decorator for method logging to console
# example:
# @logMethodToConsole('method called')
# def method(self, phrase)
#
# class.method('hello')
#
# result:
# class.testMethod(('hello',), {}) 17:59:32 - method called
def logMethodToConsole(logText):
    def funcWrapper(function):
        def funcCall(self, *args, **kwargs):
            funcName = self.getMethodName(function.__str__())
            logger.logToConsole(logText,
                                coller=self.getCaller(function.__str__()),
                                functionName=funcName,
                                args=args,
                                kwargs=kwargs)
            return function(self, *args, **kwargs)
        return funcCall
    return funcWrapper
# decorator for method logging to console
