FROM resin/raspberrypi3-debian:latest

ENV INITSYSTEM on

RUN apt-get update && apt-get install -yq \
  python3 \
  python3-sense-hat \
  wget

COPY . /usr/src/app
WORKDIR /usr/src/app

ENV dtoverlay rpi-sense

CMD ["python3", "breathe.py"]
