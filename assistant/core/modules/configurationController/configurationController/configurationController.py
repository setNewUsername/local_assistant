import json
import os.path
from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile
from core.modules.configurationController.configurationFile.configurationFile import ConfigFile
from core.modules.configurationController.configurations.configurations import Configurations


class ConfigController(LogClient):

    configurationFileName: str = None
    confgigurationDirPath: str = None

    configData: dict[str, str] = None

    languageModel: str = None
    modelFiles: str = None
    grammarFile: str = None
    dictFile: str = None

    def __init__(self, cfgFileName: str, cfgDirPath: str, logFile) -> None:
        super().__init__(logFile)
        self.configurationFileName = cfgFileName
        self.confgigurationDirPath = cfgDirPath
        self.configData = {}

    # checks for config file existence
    def checkConfigFile(self) -> bool:
        return os.path.isfile(os.path.join(self.confgigurationDirPath,
                                           self.configurationFileName))
    # checks for config file existence

    # creates empty config file
    @logMethodToFile('erasing config data')
    def recreateConfigFile(self) -> None:
        file = open(os.path.join(self.confgigurationDirPath,
                                 self.configurationFileName), 'w')
        file.close()
    # creates empty config file

    @logMethodToFile('checking config file layout')
    def checkConfigFileLayout(self, data: dict[str, str]) -> bool:
        if 'lang_model' not in data:
            return False
        if 'model_files' not in data:
            return False
        if 'grammar_file' not in data:
            return False
        if 'dictionary_file' not in data:
            return False
        if 'commands' not in data:
            return False
        if 'domains' not in data:
            return False
        return True

    # creates default config file layout if it is empty file
    @logMethodToFile('checking config file layout set default if corrupted')
    def setDefaultConfigIfEmpty(self) -> None:
        with open(os.path.join(self.confgigurationDirPath,
                               self.configurationFileName), 'r') as file:
            try:
                cfgData = json.load(file)
            except Exception as e:
                self.innerLogToFile(f'error while loading JSON {e}')
                self.configData = Configurations.DEFAULT_CONFIG.value
                self.writeDataToConfigFile()
            else:
                if not self.checkConfigFileLayout(cfgData):
                    self.innerLogToFile('corrupted config layout, recreate')
                    self.configData = Configurations.DEFAULT_CONFIG.value
                    self.writeDataToConfigFile()
    # creates default config file layout if it is empty file

    # reads config data to field configData
    @logMethodToFile('loading config data')
    def readDataFromConfigFile(self) -> None:
        with ConfigFile(
            os.path.join(self.confgigurationDirPath,
                         self.configurationFileName), 'r') as input:
            self.configData = json.load(input)
    # reads config data to field configData

    # saves config data from configData to config file
    @logMethodToFile('save config data')
    def writeDataToConfigFile(self) -> None:
        with ConfigFile(
            os.path.join(self.confgigurationDirPath,
                         self.configurationFileName), 'w') as input:
            input.write(json.dumps(self.configData))
    # saves config data from configData to config file

    # replaces commands data in configData
    @logMethodToFile('updating commands data')
    def updateCommandsData(self, data: dict[str, str]) -> None:
        self.configData['commands'] = data
    # replaces commands data in configData

    # returns commands data from configData
    def getComandsData(self) -> list:
        return self.configData['commands']
    # returns commands data from configData

    # replaces domains data in configData
    @logMethodToFile('updating domains data')
    def updateDomainsData(self, data: dict[str, str]) -> None:
        self.configData['domains'] = data
    # replaces domains data in configData

    # returns domains data from configData
    def getDomainsData(self) -> list:
        return self.configData['domains']
    # returns domains data from configData

    # returns language model name
    def getLanguageModel(self) -> str:
        return self.configData['lang_model']

    # returns language model files name
    def getModelFiles(self) -> str:
        return self.configData['model_files']

    # return grammar file name
    def getGrammarFile(self) -> str:
        return self.configData['grammar_file']

    # returns dictionary file name
    def getDictFile(self) -> str:
        return self.configData['dictionary_file']
