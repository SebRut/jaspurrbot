FROM python:3-alpine

ADD main.py /
ADD requirements.txt /

RUN git rev-parse HEAD > VERSION
RUN pip install -r requirements.txt
RUN rm requirements.txt

CMD [ "python", "./main.py" ]
