import requests
import time
from environs import Env
import logging
import telegram


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()

    bot = telegram.Bot(token=env('TELEGRAM_ACCESS_TOKEN'))
    chat_id = env('TELEGRAM_CHAT_ID')
    logger.debug(bot.get_me())

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        "Authorization": "Token " + env('DEVMAN_ACCESS_TOKEN')
    }

    timestamp_to_request = time.time()

    while True:
        try:
            params = {"timestamp": timestamp_to_request}

            response = requests.get(url, headers=headers, timeout=30, params=params)
            response.raise_for_status()

            parsed_response = response.json()
            if parsed_response['status'] == "timeout":
                timestamp_to_request = parsed_response['timestamp_to_request']
                logger.debug(f"timestamp_to_request: {timestamp_to_request}")
            elif parsed_response['status'] == "found":
                timestamp_to_request = parsed_response['last_attempt_timestamp']
                logger.debug(f"timestamp_to_request: {timestamp_to_request}")

                for attempt in parsed_response['new_attempts']:
                    result = 'К сожалению, в работе нашлись ошибки.' if attempt[
                        'is_negative'] else 'Преподавателю всё понравилось, можно приступать к следующему уроку!'
                    bot.send_message(chat_id=chat_id,
                                     text=f"""У вас проверили работу \"<a href="{attempt['lesson_url']}">{attempt['lesson_title']}</a>\".\n\n{result}""",
                                     parse_mode=telegram.ParseMode.HTML)

        except requests.exceptions.ReadTimeout:
            logger.info("Превышено время ожидания. Отправляем запрос заново...")
        except requests.exceptions.ConnectionError:
            logger.info("Интернет отключится! Отправляем запрос заново через 5 секунд...")
            time.sleep(5)

if __name__ == '__main__':
    main()