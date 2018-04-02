FROM ubuntu:latest
MAINTAINER John Lepird "jlepird@alum.mit.edu"
RUN apt-get update -y
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y
RUN apt-get install -y python3.6 python3.6-dev build-essential curl
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6
COPY . /app
WORKDIR /app
RUN pip3.6 install -r requirements.txt
ENTRYPOINT ["python3.6"]
CMD ["main.py"]
