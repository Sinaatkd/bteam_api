FROM python:3.9

WORKDIR /home/code

RUN apt-get update && apt-get install -y --no-install-recommends cron

COPY . .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

#https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
#https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/daphne/
RUN python -m pip install daphne

ENV DJANGO_SETTINGS_MODULE=bteam_api.settings

# mysql
EXPOSE 3306
#web
EXPOSE 8000


CMD [ "daphne","-b","0.0.0.0","-p","8000","bteam_api.asgi:application" ]