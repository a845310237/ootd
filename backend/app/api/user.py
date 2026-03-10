"""User profile API endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from run import db
from app.models.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile information.

    Returns:
        JSON response with user profile data
    """
    try:
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'height': user.height,
            'weight': user.weight,
            'bodyType': user.body_type,
            'skinTone': user.skin_tone,
            'avatar': user.avatar
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user's profile information.

    Request JSON:
        {
            "name": "New Name",
            "height": 175,
            "weight": 70,
            "bodyType": "标准",
            "skinTone": "中性",
            "avatar": "https://example.com/avatar.jpg"
        }

    Returns:
        JSON response with updated user data
    """
    try:
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        data = request.get_json()

        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
        if 'height' in data:
            user.height = data['height']
        if 'weight' in data:
            user.weight = data['weight']
        if 'bodyType' in data:
            user.body_type = data['bodyType']
        if 'skinTone' in data:
            user.skin_tone = data['skinTone']
        if 'avatar' in data:
            user.avatar = data['avatar']

        db.session.commit()

        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'height': user.height,
            'weight': user.weight,
            'bodyType': user.body_type,
            'skinTone': user.skin_tone,
            'avatar': user.avatar
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新用户信息失败: {str(e)}'}), 500
