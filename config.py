import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    PNG_FOLDER = os.environ.get('PNG_FOLDER', 'pngs')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB