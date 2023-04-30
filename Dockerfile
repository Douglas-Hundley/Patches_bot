FROM python:3.9
WORKDIR /bot
COPY Patches_bot/requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
CMD python Patches_bot/bot.py