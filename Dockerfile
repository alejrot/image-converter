

ARG VERSION=3.13.1-slim-bookworm 
FROM python:${VERSION}      

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt --upgrade pip

COPY .  /app       

RUN mkdir /root/input

RUN mkdir /root/output

WORKDIR /app

# goood!
# CMD ["python", "main.py", "-sf", "./examples/" , "-df", "./output/", "-kr"]
# CMD ["python", "main.py", "--help"]

# goood!
CMD ["python", "main.py", "-sf", "/root/input" , "-df", "/root/output", "-kr"]