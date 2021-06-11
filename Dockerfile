FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "hypercorn", "src/app:app", "-b", "0.0.0.0:80" ]
