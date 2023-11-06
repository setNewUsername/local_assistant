import os
from core.modules.logger.logFilesEnum import LogFiles


class LogFile:
    logFileName: str = None
    fileDescriptor = None
    logDirPath: str = None

    def __init__(self, logDir,
                 logFileName: str = LogFiles.COMMON_LOG_FILE) -> None:
        self.logFileName = logFileName.value
        self.logDirPath = logDir

    def openFile(self) -> None:
        self.fileDescriptor = open(
            os.path.join(self.logDirPath, self.logFileName), 'a')

    def closeFile(self, type, value, traceback) -> None:
        self.fileDescriptor.close()

    def fileExists(self) -> bool:
        return os.path.isfile(os.path.join(self.logDirPath, self.logFileName))
