FROM python:3.12-bullseye

ARG UID=1000
ARG GID=1000
RUN groupadd -o -g $GID automat
RUN useradd -m -u $UID -g $GID -s /bin/bash automat
WORKDIR /home/plater/automat-server/Automat

COPY ./requirements.txt /home/plater/automat-server/Automat/requirements.txt
RUN pip3 install -r /home/plater/automat-server/Automat/requirements.txt

COPY . /home/plater/automat-server/Automat/.

EXPOSE 8081
RUN mkdir -p logs
RUN rm -rf logs/*
RUN chown automat:automat logs
USER automat
ENV PYTHONPATH=/home/plater/automat-server/Automat
ENTRYPOINT ["python", "main.py"]