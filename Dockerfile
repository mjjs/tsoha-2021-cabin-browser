FROM python:3

WORKDIR /cabin-browser

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
RUN chmod +x ./launch_prod_server.sh

WORKDIR /cabin-browser/cabin-browser

CMD ["sh", "../launch_prod_server.sh"]
