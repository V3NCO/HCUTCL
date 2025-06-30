FROM python:3-alpine
COPY requirements.txt /
COPY app.py /
COPY hcul.py /
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "/app.py"]
