FROM python:3.9-slim-bookworm
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless procps curl && \
    apt-get clean;
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
WORKDIR /app
RUN pip install --no-cache-dir pyspark==3.5.0 pandas plotly streamlit cassandra-driver kafka-python numpy
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]