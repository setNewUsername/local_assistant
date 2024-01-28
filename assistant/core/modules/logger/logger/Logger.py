import os
from datetime import datetime
from core.modules.logger.logFilesEnum import LogFiles
from core.modules.logger.logFile.logFile import LogFile


class Logger:
    logsFolderPath: str = None

    commonLogFileName: str = LogFiles.COMMON_LOG_FILE
    commonLogFileDescriptor = None

    logDirPath: str = None
    liveLog: bool = False

    logFilesDescriptors: dict = None

    def __init__(self, liveLog: bool = False) -> None:
        self.logFilesDescriptors = {}
        self.liveLog = liveLog

    def concatLogsDirLogFile(self, logFileName: str) -> None:
        return os.path.join(self.logDirPath, logFileName)

    def setCommonLogDirPath(self, newLogDirName: str) -> None:
        self.logDirPath = newLogDirName

    # opens common log file
    # uses firstly to log rest of actions of logger
    def setupCommonLogFile(self) -> None:
        commonLogFile = LogFile(self.logDirPath,
                                logFileName=self.commonLogFileName)
        if not commonLogFile.fileExists():
            self.recreateFile(self.commonLogFileName)
        commonLogFile.openFile()
        self.commonLogFileDescriptor = commonLogFile.fileDescriptor
        self.logFilesDescriptors[
                                 self.commonLogFileName
                                ] = self.commonLogFileDescriptor
    # opens common log file
    # uses firstly to log rest of actions of logger

    # closes common log file
    def closeCommonLogFile(self) -> None:
        self.commonLogFileDescriptor.close()
    # closes common log file

    # adds to descriptors map new descriptor
    # recreates file if not exists
    def registerLogFile(self, logFile: LogFiles) -> None:
        if logFile not in self.logFilesDescriptors:
            newLogFile = LogFile(self.logDirPath, logFileName=logFile)
            if not newLogFile.fileExists():
                self.recreateFile(logFile)
            newLogFile.openFile()
            self.logFilesDescriptors[logFile] = newLogFile.fileDescriptor

            self.logToLogFile(logFileName=self.commonLogFileName,
                              logText=f'reg new log file {logFile}',
                              coller='logger',
                              functionName='registerLogFile')
    # adds to descriptors map new descriptor
    # recreates file if not exists

    # iterates through files descriptors map; closes them
    def unregisterLogFiles(self) -> None:
        for logFileKey in self.logFilesDescriptors.keys():
            if logFileKey != self.commonLogFileName:
                self.logToLogFile(logFileName=self.commonLogFileName,
                                  logText=f'unreg log file {logFileKey}',
                                  coller='logger',
                                  functionName='unregisterLogFiles')
                self.logFilesDescriptors[logFileKey].close()
    # iterates through files descriptors map; closes them

    # opens file to write and closes immediatly
    def recreateFile(self, logFile: str) -> None:
        file = open(os.path.join(self.logDirPath, logFile.value), 'w')
        file.close()
    # opens file to write and closes immediatly

    # checks log folder for existing
    def checkLogFolderState(self) -> bool:
        return os.path.isdir(self.logDirPath)
    # checks log folder for existing

    # writes data to log file
    # example:
    # no_caller.no_function({'no_arg': 'no_arg'}) 13:24:52 - hello world
    def logToLogFile(self,
                     logFileName: LogFiles,
                     logText: str,
                     coller: str = 'no_coller',
                     functionName: str = 'no_function',
                     args: tuple = (),
                     kwargs: dict[str, str] = {}) -> None:

        collerArgsStr = f'{coller}.{functionName}({args}, {kwargs})'
        date = datetime.now().strftime("%H:%M:%S")
        if logFileName in self.logFilesDescriptors:
            self.logFilesDescriptors[logFileName].write(f'{date} {collerArgsStr} - {logText}\n')
        else:
            self.commonLogFileDescriptor.write(f'{date} {collerArgsStr} - Unable to find log file enum {logFileName.value}; check file registration?\n')
        self.commonLogFileDescriptor.write(f'{date} {collerArgsStr} - {logText}\n')

        self.logToConsole(logText, coller=coller, functionName=functionName, args=args)
    # writes data to log file

    # writes data to console
    # example
    # no_coller.no_function({'no_arg': 'no_arg'}) 13:24:52 - hello world
    def logToConsole(self,
                     logText: str,
                     coller: str = 'no_coller',
                     functionName: str = 'no_function',
                     args: tuple = (),
                     kwargs: dict[str, str] = {}) -> None:
        collerArgsStr = f'{coller}.{functionName}({args}, {kwargs})'
        date = datetime.now().strftime("%H:%M:%S")
        if self.liveLog:
            print(f'{date} {collerArgsStr} - {logText}')
    # writes data to console


logger = Logger(liveLog=True)
