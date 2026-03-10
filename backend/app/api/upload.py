"""Upload API endpoint for image upload to OSS or local storage."""
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from run import db
from app.services.oss_service import oss_service
import uuid

upload_bp = Blueprint('upload', __name__)

# Allowed image file types
ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def _ensure_upload_dir():
    """Ensure upload directory exists."""
    upload_dir = os.getenv('UPLOAD_DIR', '/data/public/uploads')
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


@upload_bp.route('', methods=['POST'])
@jwt_required()
def upload_image():
    """
    Upload an image to OSS or local storage.

    Request: multipart/form-data with 'file' field

    Returns:
        JSON response with uploaded image URL
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400

        file = request.files['file']

        # Check if file has a filename
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400

        # Get file info
        filename = secure_filename(file.filename)
        file_content = file.read()
        content_type = file.content_type or 'image/jpeg'

        # Validate file type
        if content_type not in ALLOWED_TYPES:
            return jsonify({
                'error': f'不支持的文件类型。支持的类型: {", ".join(ALLOWED_TYPES)}'
            }), 400

        # Validate file size
        if len(file_content) > MAX_FILE_SIZE:
            return jsonify({
                'error': f'文件大小超过限制 ({MAX_FILE_SIZE / 1024 / 1024}MB)'
            }), 400

        # Try OSS upload first
        if oss_service.is_configured():
            result = oss_service.upload_file(file_content, filename, content_type)
            if result['success']:
                return jsonify({
                    'success': True,
                    'url': result['url']
                }), 200
            else:
                # Log OSS error but fall through to local storage
                print(f'OSS upload failed: {result.get("error")}, falling back to local storage')

        # Fallback to local storage
        upload_dir = _ensure_upload_dir()

        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}-{filename}"
        filepath = os.path.join(upload_dir, unique_filename)

        # Save file
        with open(filepath, 'wb') as f:
            f.write(file_content)

        # Return relative URL path
        return jsonify({
            'success': True,
            'url': f'/uploads/{unique_filename}'
        }), 200

    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500


@upload_bp.route('/base64', methods=['POST'])
@jwt_required()
def upload_base64():
    """
    Upload an image from base64 data.

    Request JSON:
        {
            "data": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
            "filename": "image.jpg" (optional)
        }

    Returns:
        JSON response with uploaded image URL
    """
    try:
        data = request.get_json()

        if not data.get('data'):
            return jsonify({'error': '缺少图片数据'}), 400

        base64_data = data['data']

        # Parse data URL
        if base64_data.startswith('data:'):
            # Extract content type and base64 string
            parts = base64_data.split(',', 1)
            if len(parts) != 2:
                return jsonify({'error': '无效的图片数据格式'}), 400

            # Extract content type from data URL
            header = parts[0]
            content_type = 'image/jpeg'  # default
            if ';' in header:
                content_type = header.split(';')[0].split(':')[1]

            base64_string = parts[1]
        else:
            # Assume raw base64 string
            content_type = 'image/jpeg'
            base64_string = base64_data

        # Validate content type
        if content_type not in ALLOWED_TYPES:
            return jsonify({
                'error': f'不支持的文件类型。支持的类型: {", ".join(ALLOWED_TYPES)}'
            }), 400

        # Decode base64
        import base64
        file_content = base64.b64decode(base64_string)

        # Validate file size
        if len(file_content) > MAX_FILE_SIZE:
            return jsonify({
                'error': f'文件大小超过限制 ({MAX_FILE_SIZE / 1024 / 1024}MB)'
            }), 400

        # Get filename
        filename = data.get('filename', 'upload.jpg')

        # Try OSS upload first
        if oss_service.is_configured():
            result = oss_service.upload_file(file_content, filename, content_type)
            if result['success']:
                return jsonify({
                    'success': True,
                    'url': result['url']
                }), 200

        # Fallback to local storage
        upload_dir = _ensure_upload_dir()
        unique_filename = f"{uuid.uuid4()}-{filename}"
        filepath = os.path.join(upload_dir, unique_filename)

        with open(filepath, 'wb') as f:
            f.write(file_content)

        return jsonify({
            'success': True,
            'url': f'/uploads/{unique_filename}'
        }), 200

    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500
