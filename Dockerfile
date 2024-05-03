ARG BASE_IMAGE=python:3.12.3
FROM --platform=linux/amd64 $BASE_IMAGE

# Set working directory as `/code/`
WORKDIR /code

# Copy python modules used within application
COPY ./requirements.txt /code/requirements.txt

# Install all python modules, keep image as small as possible
# don't store the cache directory during install
RUN pip install --no-build-isolation --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code to `/code/app/`
COPY ./app /code/app

# Don't run application as root, instead user called `nobody`
RUN chown -R nobody /code

USER nobody

# Ensure container is healthy using a healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8080/docs || exit 1

# Start fastapi application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
