ARG BASE_IMAGE=python:3.12
FROM --platform=linux/amd64 $BASE_IMAGE

# Set working directory as `/code/`
WORKDIR /code

# Copy python modules used within application
COPY ./requirements.txt /code/requirements.txt

# Install all python modules, keep image as small as possible
# don't store the cache directory during install
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code to `/code/app/`
COPY ./app /code/app

# Don't run application as root, instead user called `nobody`
RUN chown -R nobody:nobody /code

USER nobody

# Start fastapi application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
