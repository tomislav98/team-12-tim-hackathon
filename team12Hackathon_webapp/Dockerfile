FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

RUN mkdir /db

WORKDIR /code

COPY requirements.txt /code/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/

COPY start.sh /code/

# insert here your api tim url
ENV API_URL_TIM=""

# insert here your api token
ENV API_TOKEN_TIM=""

RUN chmod +x start.sh

CMD ["sh" , "-c", "./start.sh"]
