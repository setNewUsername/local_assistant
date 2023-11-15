import os
from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile


class Text2DictUtil(LogClient):
    targetWordsList: list[str] = None

    localStoragePath: str = None
    utilStorageDirName: str = 'text2dict'
    targetFileName: str = 'wordList'

    targetFileFullPath: str = None

    resultDirPath: str = None
    resultFileName: str = None

    resultFileFullPath: str = None

    dict2transcriptPath: str = None

    def __init__(self,
                 logFile,
                 transcriptScriptPath: str,
                 localStorage: str,
                 resultDir: str,
                 resultFile: str) -> None:
        super().__init__(logFile)
        self.loggerRegister()
        self.dict2transcriptPath = transcriptScriptPath

        self.localStoragePath = localStorage

        utilStorage = os.path.join(self.localStoragePath,
                                   self.utilStorageDirName)
        self.targetFileFullPath = os.path.join(utilStorage,
                                               self.targetFileName)

        self.resultDirPath = resultDir
        self.resultFileName = resultFile

        self.resultFileFullPath = os.path.join(self.resultDirPath,
                                               self.resultFileName)

    @logMethodToFile('setting new word list')
    def setWordList(self, words: list[str]) -> None:
        self.targetWordsList = words

    def checkUtilDir(self) -> bool:
        return os.path.isdir(os.path.join(self.localStoragePath,
                                          self.utilStorageDirName))

    def createUtilDir(self) -> None:
        os.mkdir(os.path.join(self.localStoragePath,
                              self.utilStorageDirName))

    def checkInputFile(self) -> bool:
        return os.path.isfile(self.targetFileFullPath)

    def createInputFile(self) -> None:
        with open(self.targetFileFullPath, 'w'):
            pass

    def checkOutputFile(self) -> bool:
        return os.path.isfile(self.resultFileFullPath)

    def createOutputFile(self) -> None:
        with open(self.resultFileFullPath, 'w'):
            pass

    def writeWordList(self) -> None:
        self.innerLogToFile('write words to input file')
        with open(self.targetFileFullPath, 'w', encoding='utf-8') as file:
            for line in self.targetWordsList:
                file.write(f'{line}\n')

    def setUp(self) -> None:
        if not self.checkUtilDir():
            self.innerLogToFile('no util dir found; create')
            self.createUtilDir()
        if not self.checkInputFile():
            self.innerLogToFile('no input file found; create')
            self.createInputFile()
        if not self.checkOutputFile():
            self.innerLogToFile('no output file found; create')
            self.createOutputFile()
        self.writeWordList()

    def translate(self) -> None:
        os.system(f'perl {self.dict2transcriptPath} {self.targetFileFullPath} {self.resultFileFullPath}')
