from core.modules.speechController.languageModels.baseLanguageModel import LanguageModel


class RuLanguageModel(LanguageModel):

    def __init__(self, modelFiles,
                 grammarFile: str = None,
                 dictFile: str = None,
                 startWord: str = 'привет') -> None:
        super().__init__()
        self.standartDictFile = 'ru.dic'
        self.standartModelFile = 'ru.lm'
        self.startWord = startWord

        self.grammarFileName = grammarFile
        self.dictionaryFile = dictFile
        self.modelFiles = modelFiles
