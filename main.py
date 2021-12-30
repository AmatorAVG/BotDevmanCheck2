import requests
import pprint

url = 'https://dvmn.org/api/user_reviews/'
url = 'https://dvmn.org/api/long_polling/'
headers = {
    "Authorization": "Token 0917402927c503bff63c66aa7cf31835c66c4a86"
}

while True:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        pprint.pprint(response.json())
    except requests.exceptions.ReadTimeout:
        print("Превышено время ожидания. Отправляем запрос заново...")


