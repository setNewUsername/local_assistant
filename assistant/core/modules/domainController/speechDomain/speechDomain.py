class SpeechDomain:

    word: str = None
    childrenDomains: list[str] = None
    parentDomainUuid: str = None
    domainUuid: str = None

    def __init__(self,
                 word: str,
                 domainUuid: str,
                 parentDomainUuid: str) -> None:
        self.word = word
        self.domainUuid = domainUuid
        self.parentDomainUuid = parentDomainUuid

        self.childrenDomains = []

    def addChildDomain(self, newChildUuid: str) -> None:
        self.childrenDomains.append(newChildUuid)

    def checkChild(self, childToCheck: str) -> bool:
        return childToCheck in self.childrenDomains

    def __str__(self) -> str:
        return f"""
        uuid: {self.domainUuid},
        word: {self.word},
        parent domain: {self.parentDomainUuid}"""

    def serialize(self) -> dict[str, str]:
        return {'domain_word': self.word,
                'parent_dom_uuid': self.parentDomainUuid,
                'domain_uuid': self.domainUuid}
