# Контейнер с необходимым для работы бота
# 1. Импортируем контейнер с питоном
# 2. Доставляем необходимые библиотеки
# 3. Устанавливаем часовой пояс

FROM python:3.8-slim

RUN apt update 
RUN apt install python3 -y
RUN apt install git -y
#RUN apt --update install gcc build-base freetype-dev libpng-dev openblas-dev
RUN apt install tzdata
ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip3 install aiogram
RUN pip3 install asyncio
RUN pip3 install aioschedule
RUN pip3 install datetime
RUN pip3 install bs4
RUN pip3 install python-dotenv
RUN pip3 install requests
RUN pip3 install --no-cache-dir matplotlib pandas