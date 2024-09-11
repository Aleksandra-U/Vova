# FROM python:3.12

# RUN mkdir /screener

# WORKDIR /screener

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind=0.0.0.0:8000"]