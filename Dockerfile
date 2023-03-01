FROM python:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/src
WORKDIR /code
RUN pip install -U pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["gunicorn", "-w", "12", "--bind", "0.0.0.0:8000", "wsgi:app"]