FROM python:3.10-slim AS compile-image

## install dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential gcc

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## add and install requirements
COPY ./requirements.txt .
RUN pip install --upgrade pip &&  \
  pip install -r requirements.txt


FROM python:3.10-slim AS build-image

# copy env from prev img
COPY --from=compile-image /opt/venv /opt/venv
WORKDIR /app
COPY . /app
RUN apt-get update -y && apt-get install -y libgomp1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

CMD ["sh", "-c" , "uvicorn api:app --host 0.0.0.0 --port 8000 --reload"]
