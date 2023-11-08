from enum import Enum


class Configurations(Enum):
    DEFAULT_CONFIG = {
        'lang_model': 'ru',
        'model_files': 'zero_ru.cd_cont_4000',
        'grammar_file': 'grammar.jsgf',
        'dictionary_file': 'dict.dic',
        'commands': [
            {
            }
        ],
        'domains': [
            {
            }
        ]
    }
