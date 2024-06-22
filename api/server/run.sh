#!/bin/bash
export DATABASE_URI=${DATABSE_URL}


# prestart checks


PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}


echo "Checking for the script in the path $PRE_START_PATH"


if [ -f $PRE_START_PATH ] ; then
    echo "Running the script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script in  $PRE_START_PATH"
fi


export APP_MODULE=${APP_MODULE:-app.main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8001}
export ENTRYPOINT=${ENTRYPOINT:-./app/main.py}


#run the python script
python "$ENTRYPOINT"
# exec gunicorn --bind $HOST:$PORT "$APP_MODULE" \
#   -k uvicorn.workers.UvicornWorker \
#   -w 4


# exec gunicorn --bind $HOST:$PORT "$APP_MODULE" -k uvicorn.workers.UvicornWorker  