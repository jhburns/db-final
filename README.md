# Airline Management Program

## Install Locally

```bash
$ python3 -m venv .env
$ source .env/bin/activate
$ python3 -m pip install -r requirements.txt
```

## Run Locally

```bash
$ cd ./src
$ uvicorn main:app --reload
```

You should get:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28485] using statreload
INFO:     Started server process [28487]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## With Docker
```bash
$ docker-compose up
```