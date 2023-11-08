from enum import Enum


class Configurations(Enum):
    DEFAULT_CONFIG = {
        'languageModel': 'ru',
        'modelFiles': 'zero_ru.cd_cont_4000',
        'grammarFile': 'grammar.jsgf',
        'dictFile': 'dict.dic',
        'commands': [
            {
            }
        ],
        'domains': [
            {
            }
        ]
    }
