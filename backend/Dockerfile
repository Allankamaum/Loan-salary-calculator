FROM python:3.13.3-slim
# When building the docker file we can use 2 codes.

# Using add will just download everything inclusive of files you didnt wwant to download.
# E.G if you had an archive file then using add will exctract the file. 

WORKDIR /app

COPY requirements.txt .
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

# This gives you more contol on how to download files. 
# Allows you to just copy files as they are without extraction as an example.

COPY . .
# Run the application

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
