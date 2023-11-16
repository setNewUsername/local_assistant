import os

from core.modules.domainController.speechDomain.speechDomain import SpeechDomain as SD

from core.modules.logger.logFuncs import logMethodToFile
from core.modules.logger.logFuncs import LogClient


class GarammarGenerator(LogClient):

    # used to share few counters between methods
    class Counter:
        curLevel = 0
        wordsBatchCount = 0

        def increaseBatchCount(self) -> None:
            self.wordsBatchCount += 1

        def getBatchCount(self) -> int:
            return self.wordsBatchCount

        def increaseLevel(self) -> None:
            self.curLevel += 1

        def getLevel(self) -> int:
            return self.curLevel

    grammarFilePath: str = None
    grammarFileName: str = None
    gramFileFullPath: str = None

    rootDomain: SD = None

    gramFileHeaders: list[str] = [
        '#JSGF V1.0;\n',
        'grammar test;\n'
    ]

    batchesLineBuffer: list[str] = None

    lineBuffer: list[str] = None

    counter: Counter = None

    def __init__(self,
                 logFile,
                 gramPath: str,
                 gramName: str,
                 rtDom: SD) -> None:
        super().__init__(logFile)

        self.grammarFilePath = gramPath
        self.grammarFileName = gramName
        self.gramFileFullPath = os.path.join(self.grammarFilePath,
                                             self.grammarFileName)

        self.rootDomain = rtDom

        self.counter = self.Counter()

        self.batchesLineBuffer = []
        self.lineBuffer = []

    def checkFile(self) -> bool:
        return os.path.isfile(self.gramFileFullPath)

    # recreates grammar file
    @logMethodToFile('setting up file')
    def setupFile(self) -> None:
        with open(self.gramFileFullPath, 'w') as file:
            for line in self.gramFileHeaders:
                file.write(line)

    # returs string with wrapped words
    # example: wrapMethodsLevel(0, ['test', 'test1'])
    # result: public <lvl0> = ( test | test );
    @logMethodToFile('wrap words from list')
    def wrapWordsLevel(self, level: int, words: list[str]) -> str:
        result = f'public <lvl{level}> = ('

        for word in words:
            tmp = word
            if word.find('+') != -1:
                tmp = f'<btc{self.counter.getBatchCount()}>'
                self.batchesLineBuffer.append(self.constructBatch(
                                                self.counter.getBatchCount(),
                                                word.split('+')))
                self.counter.increaseBatchCount()
            result += ' ' + tmp + ' |'
        result = result.removesuffix('|')
        result += ');\n'

        return result

    # returs string with wrapped words batch
    # example: wrapMethodsLevel(0, ['test', 'test1'])
    # result: public <btc0> = test test;
    @logMethodToFile('construct word batch')
    def constructBatch(self, count: int, wordBatch: list[str]) -> str:
        result = f'public <btc{count}> = '
        for word in wordBatch:
            result += f'{word} '
        result = result.removesuffix(' ')
        result += ';\n'
        return result

    # returs string with phrases
    # example: wrapMethodsLevel(1, 1, 0)
    # result: public <ph1> = <ph0> <lvl1>;
    # example: wrapMethodsLevel(0, 0, None)
    # result: public <ph0> = <lvl0>;
    @logMethodToFile('construct phrase')
    def constructPhrase(self,
                        phLvl: int,
                        prevLvl: int,
                        parentPhrase: int = None) -> str:
        result = f'public <ph{phLvl}> = '
        if parentPhrase is not None:
            result += f'<ph{parentPhrase}> '
        result += f'<lvl{prevLvl}>;\n'
        return result

    # returns line for all phrases wrapped
    # example: constructPhraseLine(4)
    # result: public<phrase> = ( <ph0> | <ph1> | <ph2> | <ph3> | <ph4> );
    @logMethodToFile('construct phrase line')
    def constructPhraseLine(self, maxPhraseLevel: int) -> str:
        result = 'public <phrase> = ('

        for ph in range(maxPhraseLevel):
            result += f' <ph{str(ph)}> |'
        result = result.removesuffix('|')
        result += ');\n'

        return result

    # returns list with domain children's words
    def getDomainChildrenAsList(self, domain: SD) -> list[str]:
        result = []

        for chDom in domain.childrenDomainsPtrs:
            result.append(chDom.word)
        self.innerLogToFile(f'return children domains {result}')
        return result

    # returns domain level as list of words
    def constructDomLevel(self,
                          domains: list[SD],
                          curLvl: Counter) -> list[str]:
        result = []
        tmp = []
        for dom in domains:
            if dom.childrenDomainsPtrs != []:
                tmp += self.getDomainChildrenAsList(dom)
        result.append(self.wrapWordsLevel(curLvl.getLevel(), tmp))
        self.innerLogToFile(f'return domain level {result}')
        return result

    # returns list with next level domains
    def collectNextLvlDomains(self, domains: list[SD]) -> list[SD]:
        result = []

        for dom in domains:
            result += dom.childrenDomainsPtrs

        return result

    # recursevly construct domain levels by root domain
    def constructDomTree(self,
                         domains: list[SD],
                         currentLevel: Counter) -> None:
        chDoms = self.collectNextLvlDomains(domains)
        if len(chDoms) != 0:
            currentLevel.increaseLevel()
            self.lineBuffer += self.constructDomLevel(domains, currentLevel)
            self.constructDomTree(chDoms, currentLevel)
        else:
            return None

    # starts constructing process
    @logMethodToFile('construct grammar file from domains')
    def constructLinesByDomTree(self) -> None:
        self.lineBuffer.append(self.wrapWordsLevel(
                                self.counter.getLevel(),
                                [self.rootDomain.word]))
        self.counter.increaseLevel()
        self.lineBuffer += self.constructDomLevel([self.rootDomain],
                                                  self.counter)
        self.constructDomTree(self.rootDomain.childrenDomainsPtrs,
                              self.counter)

    # constructs phrases
    @logMethodToFile('construct phrases')
    def constructPhrases(self) -> None:
        self.lineBuffer.append(self.constructPhrase(0, 0, None))
        for i in range(1, self.counter.getLevel() + 1, 1):
            self.lineBuffer.append(self.constructPhrase(i, i, i - 1))
        self.lineBuffer.append(self.constructPhraseLine(self.counter.getLevel() + 1))

    # initiates grammar file rebuild process
    @logMethodToFile('starting grammar file rebuild')
    def rebuild(self) -> None:
        self.setupFile()
        self.constructLinesByDomTree()
        self.constructPhrases()
        with open(self.gramFileFullPath, 'a', encoding='utf-8') as file:
            if self.batchesLineBuffer != []:
                for line in self.batchesLineBuffer:
                    file.write(f'{line}')
            for line in self.lineBuffer:
                file.write(f'{line}')
