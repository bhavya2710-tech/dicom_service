import os
from flask import current_app, request, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app.dicom_utils import extract_dicom_tag, convert_dicom_to_png

ns = Namespace('dicom', description='DICOM operations')

# Request parsers
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='DICOM file')

extract_parser = ns.parser()
extract_parser.add_argument('filename', type=str, required=True, help='Uploaded DICOM filename')
extract_parser.add_argument('tag', type=str, required=True, help='DICOM tag to extract')

convert_parser = ns.parser()
convert_parser.add_argument('filename', type=str, required=True, help='Uploaded DICOM filename')

# Response models
dicom_upload_model = ns.model('UploadResponse', {
    'message': fields.String,
    'filename': fields.String
})

tag_model = ns.model('TagResponse', {
    'tag': fields.String,
    'value': fields.String
})

@ns.route('/upload')
class DicomUpload(Resource):
    @ns.expect(upload_parser)
    @ns.marshal_with(dicom_upload_model, code=201)
    def post(self):
        """Upload a DICOM file"""
        args = upload_parser.parse_args()
        file = args['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {'message': 'File uploaded', 'filename': filename}, 201

@ns.route('/extract')
class DicomExtract(Resource):
    @ns.expect(extract_parser)
    @ns.marshal_with(tag_model)
    def get(self):
        """Extract a DICOM header tag"""
        args = extract_parser.parse_args()
        filename = args['filename']
        tag = args['tag']
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        value = extract_dicom_tag(filepath, tag)
        if value is None:
            ns.abort(400, 'Invalid tag or file not found')
        return {'tag': tag, 'value': str(value)}

@ns.route('/convert')
class DicomConvert(Resource):
    @ns.expect(convert_parser)
    @ns.produces(['image/png'])
    def get(self):
        """Convert DICOM to PNG"""
        args = convert_parser.parse_args()
        filename = args['filename']
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        output_path = convert_dicom_to_png(filepath, current_app.config['PNG_FOLDER'])
        if not output_path:
            ns.abort(500, 'Conversion failed')
        return send_file(output_path, mimetype='image/png')
