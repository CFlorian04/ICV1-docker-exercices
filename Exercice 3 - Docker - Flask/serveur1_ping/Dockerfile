FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install requests
RUN pip install Flask requests

EXPOSE 4567

CMD ["python", "serveur1_ping.py"]
