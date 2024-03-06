FROM python:3.12.2-bullseye
WORKDIR /app
RUN pip install aiogram
COPY ../vita_nail/tg_bot/ /app/
CMD [ "python3", "bot.py" ]
