FROM python:2.7

VOLUME /presented-with-comment
COPY . /presented-with-comment
WORKDIR /presented-with-comment

RUN pip install -r requirements.txt

CMD ["python", "main.py"] 
