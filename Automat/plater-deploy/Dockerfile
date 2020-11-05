FROM renciorg/plater:2.0

USER root
ENV MODE="deploy"
RUN pip install gunicorn
COPY ./main.sh /home/plater/Plater/
COPY ./heartbeat.py /home/plater/Plater/PLATER/services/
USER plater








