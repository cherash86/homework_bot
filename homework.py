import logging
import os
import time
from http import HTTPStatus

import exceptions
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.info(f'Начало отправки')
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
    except Exception as error:
        logging.error(
            f'Сообщение в Telegram не отправлено: {error}')


def get_api_answer(current_timestamp):
    """Получить статус домашней работы."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        logging.error(
            f'Сообщение с API в Telegram не отправлено: {error}')
    if response.status_code != HTTPStatus.OK:
        raise exceptions.StatusCodeError('API возвращает код, отличный от 200')
    response = response.json()
    return response


def check_response(response: dict) -> list:
    """Проверка ответа API Практикума на корректность."""
    try:
        homeworkss = response['homeworks']  # Список домашних работ
    except KeyError as key_error:
        logging.error(f'Ключ словаря не найден: {key_error}')
    if type(homeworkss) != list:
        raise TypeError
    return homeworkss


def parse_status(homework: dict) -> str:
    """Извлечение из ответа названия и статуса задания."""
    try:
        homework_name = homework.get('homework_name')
        homework_status = homework.get('status')
    except KeyError as key_error:
        logging.error(f'Ключ словаря не найден: {key_error}')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    return all([TELEGRAM_TOKEN, PRACTICUM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  # Текущее время с начала эпохи Unix
    homework_status = None

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworkss = check_response(response)
            homework = homeworkss[0]
            new_homework_status = homework.get('status')
            if new_homework_status == homework_status:
                logging.debug('Статус не изменился')
            else:
                homework_status = new_homework_status
                message = parse_status(homework)
                send_message(bot, message)
            # time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            # time.sleep(RETRY_TIME)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(
                os.path.abspath('main.log'), encoding='UTF-8')],
        format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
    )
    main()