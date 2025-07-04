# PocketHealth DICOM Microservice

A Flask‑RESTX API for uploading, extracting metadata, and converting DICOM files to PNGs.

## Features

- **Upload** DICOM files (max 50MB).
- **Extract** any DICOM header tag by name.
- **Convert** DICOM pixel data to PNG for browser viewing.
- **Swagger UI** documentation at `/`.

## Quickstart

```bash
git clone <repo-url>
cd dicom_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=main.py
flask run
