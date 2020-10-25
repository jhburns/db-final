# Copied from: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/ (With modifications)
FROM python:3.6.12-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt --quiet --disable-pip-version-check

# Run the application:
COPY ./src .
CMD ["uvicorn", "main:app"]