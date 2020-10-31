#!/bin/sh

# Меняем настройки библиотеки wand для работы с PDF
sed -i -r 's/rights="none" pattern="PDF"/rights="read" pattern="PDF"/g'  /etc/ImageMagick-6/policy.xml

# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
