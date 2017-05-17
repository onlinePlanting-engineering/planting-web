#!/bin/bash

PLANTING_ROOT="${BASH_SOURCE-$0}"
PLANTING_ROOT=`dirname ${PLANTING_ROOT}`
PLANTING_ROOT=`cd ${PLANTING_ROOT};pwd`

git pull

source ${PLANTING_ROOT}/env/bin/activate
${PLANTING_ROOT}/env/bin/pip install -r requirements.txt

${PLANTING_ROOT}/env/bin/python manage.py makemigrations 
${PLANTING_ROOT}/env/bin/python manage.py migrate

GUNICORN=${PLANTING_ROOT}/env/bin/gunicorn
LOG_PREFIX=/var/log/planting
CONFIG_FILE=${PLANTING_ROOT}/conf/config.py
PID=${LOG_PREFIX}/planting.pid
LOG=${LOG_PREFIX}/gunicorn.log

APP=planting.wsgi

cd ${PLANTING_ROOT}
${GUNICORN} -D -c ${CONFIG_FILE} --log-file ${LOG} --pid ${PID} --user ${USER} ${APP}

exit 0
