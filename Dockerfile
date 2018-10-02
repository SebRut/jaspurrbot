FROM ubuntu:16.04

ADD main.py /
ADD requirements.txt /
ADD VERSION /

RUN pip install -r requirements.txt
RUN rm requirements.txt

CMD [ "python", "./main.py" ]
