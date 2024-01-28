import peewee
from core.models.modeInterface import ModelInterface


class Configuration(peewee.Model, ModelInterface):
    lang_model = peewee.TextField(unique=True)
    model_files = peewee.TextField()
    grammar_file = peewee.TextField()
    dictionary_file = peewee.TextField()

    class Meta:
        db_table = 'configuiration'

    @staticmethod
    def fromJSONtoDB(jsonData):
        ModelInterface.addIfNone(Configuration, Configuration.lang_model,
                                 jsonData['lang_model'],
                                 lang_model=jsonData['lang_model'],
                                 model_files=jsonData['model_files'],
                                 grammar_file=jsonData['grammar_file'],
                                 dictionary_file=jsonData['dictionary_file'])

    @staticmethod
    def fromDBtoJSON() -> dict:
        confData = Configuration.get_or_none()

        result = {
            "lang_model": confData.lang_model,
            "model_files": confData.model_files,
            "grammar_file": confData.grammar_file,
            "dictionary_file": confData.dictionary_file,
        }

        return result
