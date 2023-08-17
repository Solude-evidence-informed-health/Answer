FROM python:3.10.9

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8052

CMD python app.py