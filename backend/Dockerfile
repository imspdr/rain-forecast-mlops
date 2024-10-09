FROM python:3.10

ADD main.py /root
ADD infra /root/infra
ADD requirements.txt /root

WORKDIR /root
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
