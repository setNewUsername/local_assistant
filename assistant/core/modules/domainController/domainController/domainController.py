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
        print(domainsList)
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
            parentDom.addChildDomain(newDomain.domainUuid)
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
    def checkDomainWord(self,
                        domainId: str,
                        tokens: list[str],
                        nextWordId: int) -> str:
        if nextWordId == len(tokens) - 1 and self.speechDomainsIdMap[domainId].word == tokens[nextWordId]:
            return domainId
        for chDomId in self.speechDomainsIdMap[domainId].childrenDomains:
            res = self.checkDomainWord(chDomId, tokens, nextWordId + 1)
            if res is not None:
                return res
        return None
    # recursevly checks speech str sequence

    # starts speech str sequence process
    @logMethodToFile('checking speech str')
    def findDomainCommandBySpeechStr(self, spStr: str) -> str:
        result = None
        speechTokens = spStr.split('_')

        result = self.checkDomainWord(self.rootDomain.domainUuid,
                                      speechTokens,
                                      0)

        return result
    # starts speech str sequence process
