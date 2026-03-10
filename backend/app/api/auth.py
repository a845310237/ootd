"""Authentication API endpoints for user registration, login, and logout."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session

from run import db
from app.models.user import User
from app.utils.security import hash_password, verify_password, generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Request JSON:
        {
            "email": "user@example.com",
            "password": "password123",
            "name": "User Name",
            "height": 170,
            "weight": 65,
            "bodyType": "标准",
            "skinTone": "中性"
        }

    Returns:
        JSON response with user data (excluding password)
    """
    try:
        data = request.get_json()

        # Validate required fields
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        height = data.get('height')
        weight = data.get('weight')
        body_type = data.get('bodyType')
        skin_tone = data.get('skinTone')

        if not email or not password:
            return jsonify({'error': '请输入邮箱和密码'}), 400

        # Check if user already exists
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': '该邮箱已被注册'}), 400

        # Hash password
        hashed_password = hash_password(password)

        # Create new user
        import uuid
        new_user = User(
            id=str(uuid.uuid4()),
            email=email,
            password=hashed_password,
            name=name,
            height=height,
            weight=weight,
            body_type=body_type,
            skin_tone=skin_tone
        )

        db.session.add(new_user)
        db.session.commit()

        # Return user without password
        return jsonify({
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'height': new_user.height,
            'weight': new_user.weight,
            'bodyType': new_user.body_type,
            'skinTone': new_user.skin_tone,
            'avatar': new_user.avatar
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败，请稍后重试: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user with email and password.

    Request JSON:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Returns:
        JSON response with JWT access token and user data
    """
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': '请输入邮箱和密码'}), 400

        # Find user by email
        user = db.session.query(User).filter_by(email=email).first()

        if not user or not verify_password(password, user.password):
            return jsonify({'error': '邮箱或密码错误'}), 401

        # Generate JWT token
        access_token = generate_token(user.id)

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'height': user.height,
                'weight': user.weight,
                'bodyType': user.body_type,
                'skinTone': user.skin_tone,
                'avatar': user.avatar
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'登录失败，请稍后重试: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (JWT tokens are stateless, client-side logout).

    Returns:
        JSON response confirming logout
    """
    return jsonify({'message': '登出成功'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.

    Returns:
        JSON response with current user data
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
