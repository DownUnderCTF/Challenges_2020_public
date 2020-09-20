FROM python:3.9-rc-buster

WORKDIR /bot

COPY ./challenge/requirements.txt .

RUN pip install -r requirements.txt

RUN python -m pip install -U git+https://github.com/Rapptz/discord-ext-menus

COPY ./challenge/src ./challenge/flag.txt ./challenge/dummy_notes.json ./


CMD [ "python", "-u", "bot.py" ]
