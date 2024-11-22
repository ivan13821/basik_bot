from configparser import ConfigParser
from enum import Enum

config_filename = 'config.ini'

parser = ConfigParser()




"""
Модуль для проверки и получения конфигурационных файлов

"""



def get_db_params(filename=config_filename, section='postgresql'):
    parser.read(filename, "utf-8")

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Ошибка подключения к БД! Секция {0} не найдена в файле {1}'.format(section, filename))

    
    return db






def get_tg_api_token(filename=config_filename, section='telegram'):
    parser.read(filename, "utf-8")


    if parser.has_section(section):
        token = parser.get(section, 'api_token')
    else:
        raise Exception('Ошибка получения API токена бота. Секция {0} не найдена в файле {1}'.format(section, filename))


    return token






def get_feedback_chat_id(filename=config_filename, section='telegram'):
    parser.read(filename, "utf-8")

    if parser.has_section(section):
        chat_id = parser.get(section, 'feedback_chat_id')
    else:
        raise Exception('Ошибка настройки обратной связи! Секция {0} не найдена в файле {1}'.format(section, filename))

    return chat_id




def get_frequency_spam(filename=config_filename, section='spam'):
    parser.read(filename, "utf-8")

    if parser.has_section(section):
        chat_id = parser.get(section, 'frequency')
    else:
        raise Exception('Ошибка настройки обратной связи! Секция {0} не найдена в файле {1}'.format(section, filename))

    return chat_id