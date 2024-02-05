FROM kureed/enveroment:v3

WORKDIR /bot

COPY ./ ./

CMD [ "python3", "/bot/bot_start.py" ]
