__author__ = "Vitali Muladze"

import configparser
from flask import Flask

config = configparser.ConfigParser()
config.read("config.ini")


class DataBase:
    database: str = config["MONGO_CONFIG"]["DATABASE"]
    host: str = config["MONGO_CONFIG"]["HOST"]
    port: int = int(config["MONGO_CONFIG"]["PORT"])


class ApplicationConfig:
    SECRET_KEY: str = config["APPLICATION"]["SECRET_KEY"]
    WTF_CSRF_SECRET_KEY: str = config["APPLICATION"]["WTF_CSRF_SECRET_KEY"]
    MONGO_URI: str = config["APPLICATION"]["MONGO_URI"].format(host=DataBase.host,
                                                               port=DataBase.port,
                                                               database=DataBase.database)

    @staticmethod
    def init_app(app: Flask):
        pass
