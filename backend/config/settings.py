from os import environ

DATABASE_URL = environ.get("DATABASE_URL")
SECRET_KEY = environ.get("SECRET_KEY")

EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = environ.get("EMAIL_PORT")

REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")

RABBITMQ = {
    "PROTOCOL": "amqp",
    "HOST": environ.get("RABBITMQ_HOST"),
    "PORT": environ.get("RABBITMQ_PORT"),
    "USER": environ.get("RABBITMQ_USER"),
    "PASSWORD": environ.get("RABBITMQ_PASSWORD"),
}

CELERY_BROKER_URL = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}"
    f":{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)
