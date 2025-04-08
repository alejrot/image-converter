

ARG VERSION=3.13.1-slim-bookworm 
FROM python:${VERSION}      

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --upgrade pip

COPY .  /code       

# goood!
# CMD ["python", "main.py", "-sf", "./examples/" , "-df", "./output/", "-kr"]
# CMD ["python", "main.py", "--help"]

# goood!
CMD ["python", "main.py", "-sf", "examples/" , "-df", "output/", "-kr"]