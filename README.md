# Long Polling Devman's Service Tasks Checking Client

Many generations of students have taken courses on programming in Devman. And they liked everything, except for one thing: there were no notifications about checked tasks. To find out the status of my work, you had to go to the site - it is inconvenient and somehow ineffective.

Devman takes care of the students. Therefore, upon learning about such a problem, they made a special service where you can send your request. And quickly get the status of the task in response to “has my work already been checked?”.

This script is a client of the service.

### How to install

Download code:
```sh
git clone https://github.com/AmatorAVG/BotDevmanCheck2.git
```
Go to the project directory:
```sh
cd BotDevmanCheck2
```
In the project directory create virtual environment:
```sh
python -m venv venv
```
Activate it:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

Install dependencies in virtual environment:
```sh
pip install -r requirements.txt
```

In the project directory create a file `.env` containing:

- `DEVMAN_ACCESS_TOKEN` — API personal token, which you can get on [Devman site](https://dvmn.org/api/docs/).
- `TELEGRAM_ACCESS_TOKEN` — Telegram Bot API key, received by you after registering the bot at [Bot Father](https://telegram.me/BotFather).
- `TELEGRAM_CHAT_ID` — To obtain your `chat_id`, text in Telegram to special bot: `@userinfobot`.

Start the script:
```sh
python main.py
```

### How to deploy

Register on [Heroku site](https://id.heroku.com/login) and create an app.

Link your GitHub account to Heroku and press Deploy Branch on the Deploy tab.

Create Procfile and enable it on the Resources tab:
```sh
bot python3 main.py
```
Fill in the Config Vars previously specified in the .env file in the Settings tab.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).