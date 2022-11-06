# Install base image. Optimized for Python.
FROM python:3.7-slim-buster
# RUN apt-get update && apt-get install gcc g++ -y && apt-get clean
RUN pip install gradio
ADD . /app
WORKDIR /app
CMD ["python", "app.py"]
