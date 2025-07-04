import os
from flask import Flask
from flask_restx import Api
from config import Config
from logging_setup import setup_logging

setup_logging()
api = Api(
    title='PocketHealth DICOM API',
    version='1.0',
    description='API to upload, extract, and convert DICOM files'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api.init_app(app)

    # Ensure upload and png directories exist
    for folder in [app.config['UPLOAD_FOLDER'], app.config['PNG_FOLDER']]:
        os.makedirs(folder, exist_ok=True)

    # Register namespaces
    from app.routes import ns as dicom_namespace
    api.add_namespace(dicom_namespace, path='/dicom')

    return app
