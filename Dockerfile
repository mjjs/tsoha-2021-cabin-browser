FROM python:3

WORKDIR /cabin-browser
COPY . .
RUN pip3 install -r requirements.txt
WORKDIR /cabin-browser/cabin-browser

CMD ["python3", "./app.py"]
