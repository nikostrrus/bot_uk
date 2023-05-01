FROM kureed/enveroment:v1

WORKDIR /bot

COPY . .

CMD [ "python3", "bot_start.py" ]