FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev
RUN apt-get update -y && \
    apt-get install -y libmysqlclient-dev && \ 
    apt-get install -y libmariadb-dev-compat && \
    apt-get install -y libmariadbclient-dev
COPY ./app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY ./app/. /app
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=project
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV DB_HOST=db
CMD [ "flask", "run" ]
