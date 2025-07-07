import logging
logger = logging.getLogger(__name__) # создаёт логгер с именем текущего модул

logger.info("Это информационное сообщение")
logger.warning("Это предупреждение")
logger.error("Произошла ошибка")
logger.debug("Отладочная информация")
logger.critical("Критическая ошибка")
'''
Подключение логирования в файлы
def some_function():
    logger.info("Это информационное сообщение")
    logger.warning("Это предупреждение")
    logger.error("Произошла ошибка")'''