from loguru import logger as log
import sys

def add_stdout():
    # Вывод в консоль (stdout) с цветом и другим уровнем:
    log.add(
        sys.stdout,            # Приемник - стандартный вывод
        level="TRACE",         # Показывать сообщения от DEBUG и выше
        colorize=True,         # Включить цвета
        backtrace=True,        # Всегда включать подробный стектрейс (если есть)
        diagnose=True,          # Включать значения переменных в стектрейс (может быть медленно)
        format="<blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
    )


def add_serialize():
    # Структурированное логирование (JSON) - ИДЕАЛЬНО для Docker и систем агрегации:
    log.add(
        sys.stderr,             # Вывод в stderr (стандарт для Docker)
        level="TRACE",
        serialize=True          # Вывод в формате JSON
    )


def log_test():
    log.trace("Это сообщение для отладки (по умолчанию не видно)")
    log.debug("Это сообщение для отладки (по умолчанию не видно)")
    log.info("Какая-то информационная заметка")
    log.warning("Предупреждение, что-то может пойти не так")
    log.error("Произошла ошибка, но программа может продолжать работу")
    log.critical("Критическая ошибка, программа, скорее всего, упадет")

    try:
        variable = 0
        result = 1 / variable
    except ZeroDivisionError:
        log.exception("Произошло исключение!") # Автоматически добавит стектрейс

# Initialization
log.remove()
add_stdout()

