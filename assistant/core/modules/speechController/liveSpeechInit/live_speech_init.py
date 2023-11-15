import os
from core.modules.speechController.languageModels.baseLanguageModel import LanguageModel
from pocketsphinx import LiveSpeech, get_model_path


def initLiveSpeech(model: LanguageModel):
    model_path = get_model_path()

    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, model.modelFiles),
        lm=os.path.join(model_path, 'ru.lm') if model.grammarFileName is None else False,
        jsgf=None if model.grammarFileName is None else os.path.join(model_path, model.grammarFileName),
        dic=os.path.join(model_path, model.standartDictFile if model.dictionaryFile is None else model.dictionaryFile)
    )

    return speech


def startProcessSpeech(speech, handleFunction):
    print("Say something!")

    for phrase in speech:
        handleFunction(str(phrase))
