import textwrap
import requests
import time
from environs import Env
import logging
import telegram

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)


def main():

    env = Env()
    env.read_env()

    bot = telegram.Bot(token=env('TELEGRAM_ACCESS_TOKEN'))
    chat_id = env('TELEGRAM_CHAT_ID')
    logger.debug(bot.get_me())

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        "Authorization": f"Token {env('DEVMAN_ACCESS_TOKEN')}"
    }

    timestamp_to_request = time.time()

    while True:
        try:
            params = {"timestamp": timestamp_to_request}

            response = requests.get(url, headers=headers, timeout=30, params=params)
            response.raise_for_status()

            work_checks = response.json()
            if work_checks['status'] == "timeout":
                timestamp_to_request = work_checks['timestamp_to_request']
                logger.debug(f"timestamp_to_request: {timestamp_to_request}")
            elif work_checks['status'] == "found":
                timestamp_to_request = work_checks['last_attempt_timestamp']
                logger.debug(f"timestamp_to_request: {timestamp_to_request}")

                for attempt in work_checks['new_attempts']:
                    result = (
                        'К сожалению, в работе нашлись ошибки.'
                        if attempt['is_negative']
                        else 'Преподавателю всё понравилось, можно приступать к следующему уроку!'
                    )
                    bot.send_message(chat_id=chat_id,
                                     text=textwrap.dedent(f"""\
                                     У вас проверили работу \"<a href="{attempt['lesson_url']}">{attempt['lesson_title']}</a>\".
                                     
                                     {result}"""),
                                     parse_mode=telegram.ParseMode.HTML)

        except requests.exceptions.ReadTimeout:
            logger.info("Превышено время ожидания. Отправляем запрос заново...")
        except requests.exceptions.ConnectionError:
            logger.info("Интернет отключится! Отправляем запрос заново через 5 секунд...")
            time.sleep(5)


if __name__ == '__main__':
    main()
