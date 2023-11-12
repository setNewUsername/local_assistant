class SpeechPreprocessor:

    tokensBatchesList: list[str] = None

    def __init__(self, tknsBatList: list[str] = []) -> None:
        self.tokensBatchesList = tknsBatList

    def processSpeech(self, speechStr: str) -> str:

        for batch in self.tokensBatchesList:
            spaceBatch = batch.replace('+', ' ')
            startIndex = speechStr.find(spaceBatch)
            if startIndex != -1:
                endIndex = startIndex+len(batch)
                speechStr = speechStr[:startIndex] + speechStr[startIndex:endIndex].replace(' ', '+') + speechStr[endIndex + 1:]
                speechStr = speechStr[:startIndex] + f'"{speechStr[startIndex]}' + speechStr[startIndex + 1:]
                speechStr = speechStr[:endIndex] + f'{speechStr[endIndex]}"' + speechStr[endIndex + 1:]

        speechStr = speechStr.replace(' ', '_')

        return speechStr
