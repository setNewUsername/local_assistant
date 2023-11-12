from core.modules.speechController.liveSpeechInit.live_speech_init import initLiveSpeech
from core.modules.speechController.liveSpeechInit.live_speech_init import startProcessSpeech
from core.modules.speechController.speechPreprocessor.speechPreprocessor import SpeechPreprocessor
from core.modules.domainController.domainController.domainController import SpeechDomainsController
from core.modules.commandsController.commandsController.commandsController import CommandController

from core.modules.speechController.languageModels.baseLanguageModel import LanguageModel
from core.modules.speechController.languageModels.ruLangModel import RuLanguageModel

from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile


class SpeechController(LogClient):

    # live speech settings
    grammarFile: str = None
    dictFile: str = None
    lang: str = None
    modelFiles: str = None
    # live speech settings

    speechPreprocessor: SpeechPreprocessor = None
    domCntr: SpeechDomainsController = None
    comCntr: CommandController = None

    def __init__(self,
                 logFile,
                 spPrep: SpeechPreprocessor,
                 domCntr: SpeechDomainsController,
                 comCntr: CommandController) -> None:
        # log init
        super().__init__(logFile)
        self.loggerRegister()
        # log init

        self.speechPreprocessor = spPrep
        self.domCntr = domCntr
        self.comCntr = comCntr

    def createLangModel(self) -> LanguageModel:
        match self.lang:
            case 'ru':
                return self.createRuModel()
            case _:
                return None

    def createRuModel(self) -> RuLanguageModel:
        return RuLanguageModel(
            self.modelFiles,
            grammarFile=self.grammarFile,
            dictFile=self.dictFile,
            startWord=self.domCntr.rootDomain.word
        )

    def setGrammarFile(self, gramFile: str) -> None:
        self.grammarFile = gramFile

    def setDictFile(self, dictF: str) -> None:
        self.dictFile = dictF

    def setLang(self, lang: str) -> None:
        self.lang = lang

    def setModelFiles(self, mdFiles: str) -> None:
        self.modelFiles = mdFiles

    @logMethodToFile('processing speech')
    def listenFunc(self, speechStr: str) -> None:
        processedStr = self.speechPreprocessor.processSpeech(speechStr)
        print(processedStr)
        domain = self.domCntr.findDomainCommandBySpeechStr(processedStr)
        if domain is not None:
            command = self.domCntr.speechDomainsCommandIdMap[domain]
            self.comCntr.callCommandByUuid(command)

    def startListening(self) -> None:
        sp = initLiveSpeech(self.createLangModel())
        startProcessSpeech(sp, self.listenFunc)
