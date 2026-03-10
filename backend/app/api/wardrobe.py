"""Wardrobe API endpoints for clothing management."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from run import db
from app.models.user import User
from app.models.clothing import Clothing
from app.utils.helpers import json_parse, json_dumps
import uuid

wardrobe_bp = Blueprint('wardrobe', __name__)


def _clothing_to_dict(clothing: Clothing) -> dict:
    """Convert Clothing model to dictionary."""
    return {
        'id': clothing.id,
        'name': clothing.name,
        'category': clothing.category,
        'color': json_parse(clothing.color),
        'style': json_parse(clothing.style),
        'season': json_parse(clothing.season),
        'brand': clothing.brand,
        'size': clothing.size,
        'material': clothing.material,
        'imageUrl': clothing.image_url,
        'userId': clothing.user_id,
        'createdAt': clothing.created_at.isoformat() if clothing.created_at else None,
        'updatedAt': clothing.updated_at.isoformat() if clothing.updated_at else None
    }


@wardrobe_bp.route('', methods=['GET'])
@jwt_required()
def get_clothes():
    """
    Get all clothing items for current user.

    Query params:
        category: Filter by category (optional)

    Returns:
        JSON response with list of clothing items
    """
    try:
        user_id = get_jwt_identity()
        category = request.args.get('category')

        query = db.session.query(Clothing).filter_by(user_id=user_id)

        if category:
            query = query.filter_by(category=category)

        clothes = query.order_by(Clothing.created_at.desc()).all()

        return jsonify({
            'items': [_clothing_to_dict(c) for c in clothes],
            'count': len(clothes)
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取衣物列表失败: {str(e)}'}), 500


@wardrobe_bp.route('', methods=['POST'])
@jwt_required()
def add_clothing():
    """
    Add a new clothing item.

    Request JSON:
        {
            "name": "White T-shirt",
            "category": "上衣",
            "color": ["白色"],
            "style": ["休闲"],
            "season": ["春", "夏"],
            "brand": "Uniqlo",
            "size": "M",
            "material": "Cotton",
            "imageUrl": "https://example.com/image.jpg"
        }

    Returns:
        JSON response with created clothing item
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        if not data.get('name') or not data.get('category') or not data.get('imageUrl'):
            return jsonify({'error': '缺少必填字段'}), 400

        # Create new clothing item
        new_clothing = Clothing(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=data['name'],
            category=data['category'],
            color=json_dumps(data.get('color', [])),
            style=json_dumps(data.get('style', [])),
            season=json_dumps(data.get('season', [])),
            brand=data.get('brand'),
            size=data.get('size'),
            material=data.get('material'),
            image_url=data['imageUrl']
        )

        db.session.add(new_clothing)
        db.session.commit()

        return jsonify(_clothing_to_dict(new_clothing)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'添加衣物失败: {str(e)}'}), 500


@wardrobe_bp.route('/<clothing_id>', methods=['DELETE'])
@jwt_required()
def delete_clothing(clothing_id: str):
    """
    Delete a clothing item.

    Args:
        clothing_id: ID of the clothing item to delete

    Returns:
        JSON response confirming deletion
    """
    try:
        user_id = get_jwt_identity()

        # Find clothing and verify ownership
        clothing = db.session.query(Clothing).filter_by(
            id=clothing_id,
            user_id=user_id
        ).first()

        if not clothing:
            return jsonify({'error': '衣物不存在或无权删除'}), 404

        db.session.delete(clothing)
        db.session.commit()

        return jsonify({'message': '衣物已删除'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除衣物失败: {str(e)}'}), 500


@wardrobe_bp.route('/<clothing_id>', methods=['PUT'])
@jwt_required()
def update_clothing(clothing_id: str):
    """
    Update a clothing item.

    Args:
        clothing_id: ID of the clothing item to update

    Request JSON:
        {
            "name": "Updated Name",
            "category": "上衣",
            "color": ["白色", "灰色"],
            "style": ["休闲"],
            "season": ["春", "夏"],
            "brand": "Updated Brand",
            "size": "L",
            "material": "Cotton",
            "imageUrl": "https://example.com/new-image.jpg"
        }

    Returns:
        JSON response with updated clothing item
    """
    try:
        user_id = get_jwt_identity()

        # Find clothing and verify ownership
        clothing = db.session.query(Clothing).filter_by(
            id=clothing_id,
            user_id=user_id
        ).first()

        if not clothing:
            return jsonify({'error': '衣物不存在或无权修改'}), 404

        data = request.get_json()

        # Update fields if provided
        if 'name' in data:
            clothing.name = data['name']
        if 'category' in data:
            clothing.category = data['category']
        if 'color' in data:
            clothing.color = json_dumps(data['color'])
        if 'style' in data:
            clothing.style = json_dumps(data['style'])
        if 'season' in data:
            clothing.season = json_dumps(data['season'])
        if 'brand' in data:
            clothing.brand = data['brand']
        if 'size' in data:
            clothing.size = data['size']
        if 'material' in data:
            clothing.material = data['material']
        if 'imageUrl' in data:
            clothing.image_url = data['imageUrl']

        db.session.commit()

        return jsonify(_clothing_to_dict(clothing)), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新衣物失败: {str(e)}'}), 500
