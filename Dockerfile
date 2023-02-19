FROM python:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN pip install -U pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["python3", "src/main.py"]