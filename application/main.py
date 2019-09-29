__author__ = "Vitali Muladze"

from apps import create_app
from source.configuration import ApplicationConfig
from source.utils import insert_csv_files_to_mongo

application = create_app(ApplicationConfig)


application.before_first_request(insert_csv_files_to_mongo)


if __name__ == '__main__':
    application.run("0.0.0.0", "5000")
