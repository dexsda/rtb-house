FROM python:3
ADD service/ /app
WORKDIR /app
RUN apt-get update --allow-unauthenticated
RUN pip install -r requirements.txt
CMD python service.py
