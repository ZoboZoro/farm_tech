FROM python:3.12

WORKDIR /src
COPY requirements.txt src  /src/
RUN pip install --no-cache-dir -r requirements.txt
# ENTRYPOINT ["python3"]
CMD ["python3", "pipeline.py"]
EXPOSE 5000
