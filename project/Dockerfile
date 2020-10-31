# pull official base image
FROM python:3.7

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr wget antiword libmagickwand-dev ghostscript
ENV TESSDATA_PREFIX /usr/share/tesseract-ocr/4.00/tessdata/
RUN cd /usr/share/tesseract-ocr/4.00/tessdata/ && wget https://github.com/tesseract-ocr/tessdata/raw/3.04.00/rus.traineddata

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
