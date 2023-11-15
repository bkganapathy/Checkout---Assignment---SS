FROM python:latest
WORKDIR /checkout
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src src
EXPOSE 5000
ENTRYPOINT ["python", "./src/checkout.py"]
