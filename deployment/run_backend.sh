set -x
cd ${APP_ROOT_DIR}
gunicorn -w ${APP_WORKERS} -b ${APP_HOSTNAME}:${APP_PORT} --threads ${APP_THREADS} "app:app"