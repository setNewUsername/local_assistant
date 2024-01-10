from core.modules.domainController.speechDomain.speechDomain import SpeechDomain
from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile


class SpeechDomainsController(LogClient):

    speechDomainsIdMap: dict[str, SpeechDomain] = None
    speechDomainsCommandIdMap: dict[str, str] = None

    wordsRegistry: list[str] = None

    rootDomain: SpeechDomain = None

    def __init__(self, logFile) -> None:
        super().__init__(logFile)
        self.speechDomainsIdMap = {}
        self.speechDomainsCommandIdMap = {}
        self.loggerRegister()

    # sets root domain of dom tree
    @logMethodToFile('setting root domain')
    def setRootDomain(self, rootDomainData: dict[str, str]) -> None:
        self.rootDomain = self.createDomain(rootDomainData['domain_word'],
                                            rootDomainData['domain_uuid'],
                                            'none')
        self.speechDomainsCommandIdMap[self.rootDomain.domainUuid] = rootDomainData['command_uuid']
        self.speechDomainsIdMap[self.rootDomain.domainUuid] = self.rootDomain
    # sets root domain of dom tree

    # returns object of domain
    @logMethodToFile('creating new domain')
    def createDomain(self,
                     domainWord: str,
                     domainUuid: str,
                     parentDomainUuid: str) -> SpeechDomain:
        return SpeechDomain(domainWord, domainUuid, parentDomainUuid)
    # returns object of domain

    # adds domains from list
    @logMethodToFile('adding domains from list')
    def addDomains(self, domainsList: list) -> None:
        self.setRootDomain(domainsList[0])
        for domIndex in range(1, len(domainsList), 1):
            self.addDomain(domainsList[domIndex])
    # adds domains from list

    # adds new domain to dom tree,
    # speechDomainsIdMap and speechDomainsCommandIdMap
    @logMethodToFile('adding new domain to dom tree')
    def addDomain(self, domainData: dict[str, str]) -> None:
        domWord = domainData['domain_word']
        domUuid = domainData['domain_uuid']
        parentUuid = domainData['parent_dom_uuid']

        newDomain = self.createDomain(domWord, domUuid, parentUuid)

        if newDomain.parentDomainUuid in self.speechDomainsIdMap:
            self.innerLogToFile('found parent in speechDomainsIdMap')
            self.speechDomainsIdMap[newDomain.domainUuid] = newDomain
            self.speechDomainsCommandIdMap[newDomain.domainUuid] = domainData['command_uuid']

            parentDom = self.speechDomainsIdMap[newDomain.parentDomainUuid]
            parentDom.addChildDomain(newDomain.domainUuid,
                                     newChildPrt=newDomain)
        else:
            self.innerLogToFile(f'parent not found {newDomain}')
    # adds new domain to dom tree,
    # speechDomainsIdMap and speechDomainsCommandIdMap

    # returns dict of all domains fields
    # adds command uuid to result
    def serializeDomains(self) -> list:
        result: list = []

        rootData = self.rootDomain.serialize()
        rootData['command_uuid'] = self.speechDomainsCommandIdMap[self.rootDomain.domainUuid]

        result.append(rootData)

        for domainId in self.speechDomainsIdMap.keys():
            if domainId != self.rootDomain.domainUuid:
                domData = self.speechDomainsIdMap[domainId].serialize()
                domData['command_uuid'] = self.speechDomainsCommandIdMap[domainId]

                result.append(domData)

        return result
    # returns dict of all domains fields
    # adds command uuid to result

    # recursevly checks speech str sequence
    def findDomainByStr(self,
                        domainsUuids: list[str],
                        tokens: list[str],
                        currentIndex: int) -> SpeechDomain:
        if currentIndex < len(tokens):
            wordToCheck = tokens[currentIndex]
            for uuid in domainsUuids:
                if self.speechDomainsIdMap[uuid].word == wordToCheck:
                    if currentIndex == len(tokens) - 1:
                        return uuid
                    return self.findDomainByStr(self.speechDomainsIdMap[uuid].childrenDomains,
                                                tokens,
                                                currentIndex + 1)
        return None
    # recursevly checks speech str sequence

    # starts speech str sequence process
    @logMethodToFile('checking speech str')
    def findDomainCommandBySpeechStr(self, spStr: str) -> str:
        result = None
        speechTokens = spStr.split('_')
        for tokIndex in range(len(speechTokens)):
            speechTokens[tokIndex] = speechTokens[tokIndex].replace('"', '')

        if speechTokens[0] == self.rootDomain.word:
            result = self.findDomainByStr(self.rootDomain.childrenDomains, speechTokens, 1)
        return result
    # starts speech str sequence process

    def getDomainsBatches(self) -> list[str]:
        result = []

        for domainKey in self.speechDomainsIdMap:
            if self.speechDomainsIdMap[domainKey].word.find('+') != -1:
                result.append(self.speechDomainsIdMap[domainKey].word)

        return result

    def getWordList(self) -> list[str]:
        result = []
        for domUuid in self.speechDomainsIdMap.keys():
            word = self.speechDomainsIdMap[domUuid].word
            result += word.split('+')
        return result
