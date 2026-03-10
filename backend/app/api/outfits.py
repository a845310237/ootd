"""Outfits API endpoints for outfit management and AI generation."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from run import db
from app.models.user import User
from app.models.clothing import Clothing
from app.models.outfit import Outfit
from app.models.outfit_item import OutfitItem
from app.utils.helpers import json_parse, json_dumps
from app.services.tongyi_service import generate_outfit_recommendation
import uuid

outfits_bp = Blueprint('outfits', __name__)


def _outfit_to_dict(outfit: Outfit, include_items: bool = True) -> dict:
    """Convert Outfit model to dictionary."""
    result = {
        'id': outfit.id,
        'userId': outfit.user_id,
        'name': outfit.name,
        'style': outfit.style,
        'occasion': outfit.occasion,
        'season': outfit.season,
        'aiGenerated': outfit.ai_generated,
        'resultUrl': outfit.result_url,
        'prompt': outfit.prompt,
        'reasoning': outfit.reasoning,
        'tips': json_parse(outfit.tips),
        'createdAt': outfit.created_at.isoformat() if outfit.created_at else None,
        'updatedAt': outfit.updated_at.isoformat() if outfit.updated_at else None
    }

    if include_items:
        # Get outfit items
        outfit_items = db.session.query(OutfitItem).filter_by(outfit_id=outfit.id).all()
        clothing_ids = [item.clothing_id for item in outfit_items]

        # Get clothing details
        clothes = db.session.query(Clothing).filter(Clothing.id.in_(clothing_ids)).all()
        result['items'] = [
            {
                'id': c.id,
                'name': c.name,
                'category': c.category,
                'color': json_parse(c.color),
                'style': json_parse(c.style),
                'season': json_parse(c.season),
                'imageUrl': c.image_url
            }
            for c in clothes
        ]

    return result


@outfits_bp.route('', methods=['GET'])
@jwt_required()
def get_outfits():
    """
    Get all outfits for current user.

    Returns:
        JSON response with list of outfits
    """
    try:
        user_id = get_jwt_identity()
        outfits = db.session.query(Outfit).filter_by(
            user_id=user_id
        ).order_by(Outfit.created_at.desc()).all()

        return jsonify({
            'items': [_outfit_to_dict(o, include_items=False) for o in outfits],
            'count': len(outfits)
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取搭配列表失败: {str(e)}'}), 500


@outfits_bp.route('/<outfit_id>', methods=['GET'])
@jwt_required()
def get_outfit(outfit_id: str):
    """
    Get a specific outfit with details.

    Args:
        outfit_id: ID of the outfit to retrieve

    Returns:
        JSON response with outfit details including items
    """
    try:
        user_id = get_jwt_identity()
        outfit = db.session.query(Outfit).filter_by(
            id=outfit_id,
            user_id=user_id
        ).first()

        if not outfit:
            return jsonify({'error': '搭配不存在'}), 404

        return jsonify(_outfit_to_dict(outfit, include_items=True)), 200

    except Exception as e:
        return jsonify({'error': f'获取搭配详情失败: {str(e)}'}), 500


@outfits_bp.route('/<outfit_id>', methods=['DELETE'])
@jwt_required()
def delete_outfit(outfit_id: str):
    """
    Delete an outfit.

    Args:
        outfit_id: ID of the outfit to delete

    Returns:
        JSON response confirming deletion
    """
    try:
        user_id = get_jwt_identity()
        outfit = db.session.query(Outfit).filter_by(
            id=outfit_id,
            user_id=user_id
        ).first()

        if not outfit:
            return jsonify({'error': '搭配不存在或无权删除'}), 404

        db.session.delete(outfit)
        db.session.commit()

        return jsonify({'message': '搭配已删除'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除搭配失败: {str(e)}'}), 500


@outfits_bp.route('/create', methods=['POST'])
@jwt_required()
def create_outfit():
    """
    Manually create a new outfit (DIY).

    Request JSON:
        {
            "name": "Summer Casual",
            "style": "休闲",
            "occasion": "日常",
            "season": "夏",
            "itemIds": ["clothing-id-1", "clothing-id-2", ...]
        }

    Returns:
        JSON response with created outfit
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        if not data.get('name') or not data.get('itemIds'):
            return jsonify({'error': '缺少必填字段'}), 400

        # Verify all clothing items belong to user
        clothes = db.session.query(Clothing).filter(
            Clothing.id.in_(data['itemIds']),
            Clothing.user_id == user_id
        ).all()

        if len(clothes) != len(data['itemIds']):
            return jsonify({'error': '部分衣物不存在或无权访问'}), 400

        # Create outfit
        new_outfit = Outfit(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=data['name'],
            style=data.get('style', ''),
            occasion=data.get('occasion'),
            season=data.get('season'),
            ai_generated=False
        )

        db.session.add(new_outfit)
        db.session.flush()  # Get the outfit ID

        # Create outfit items
        for clothing_id in data['itemIds']:
            outfit_item = OutfitItem(
                id=str(uuid.uuid4()),
                outfit_id=new_outfit.id,
                clothing_id=clothing_id
            )
            db.session.add(outfit_item)

        db.session.commit()

        return jsonify(_outfit_to_dict(new_outfit, include_items=True)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建搭配失败: {str(e)}'}), 500


@outfits_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_outfit():
    """
    Generate an outfit recommendation using AI.

    Request JSON:
        {
            "style": "休闲",
            "occasion": "日常",
            "season": "夏"
        }

    Returns:
        JSON response with AI-generated recommendation (not saved yet)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        if not data.get('style') or not data.get('occasion') or not data.get('season'):
            return jsonify({'error': '缺少必填字段'}), 400

        # Get user info
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404

        # Get user's clothes
        clothes = db.session.query(Clothing).filter_by(user_id=user_id).all()

        if not clothes:
            return jsonify({'error': '请先添加衣物到衣柜'}), 400

        # Convert clothes to dict format
        clothes_dict = [
            {
                'id': c.id,
                'name': c.name,
                'category': c.category,
                'color': json_parse(c.color),
                'style': json_parse(c.style),
                'season': json_parse(c.season),
                'imageUrl': c.image_url
            }
            for c in clothes
        ]

        # User info for AI
        user_dict = {
            'height': user.height or 170,
            'weight': user.weight or 65,
            'bodyType': user.body_type or '标准',
            'skinTone': user.skin_tone or '中性'
        }

        # Requirements for AI
        requirements = {
            'style': data['style'],
            'occasion': data['occasion'],
            'season': data['season']
        }

        # Call AI service
        recommendation = generate_outfit_recommendation(user_dict, clothes_dict, requirements)

        # Get selected clothing details
        selected_clothes = [c for c in clothes_dict if c['id'] in recommendation['selected_items']]

        return jsonify({
            'selected_items': selected_clothes,
            'reasoning': recommendation['reasoning'],
            'tips': recommendation['tips'],
            'requirements': requirements
        }), 200

    except Exception as e:
        return jsonify({'error': f'生成搭配失败: {str(e)}'}), 500


@outfits_bp.route('/save', methods=['POST'])
@jwt_required()
def save_generated_outfit():
    """
    Save an AI-generated outfit.

    Request JSON:
        {
            "name": "AI Generated Outfit",
            "style": "休闲",
            "occasion": "日常",
            "season": "夏",
            "itemIds": ["clothing-id-1", "clothing-id-2", ...],
            "reasoning": "AI generated reasoning...",
            "tips": ["tip1", "tip2"]
        }

    Returns:
        JSON response with saved outfit
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        if not data.get('name') or not data.get('itemIds'):
            return jsonify({'error': '缺少必填字段'}), 400

        # Verify all clothing items belong to user
        clothes = db.session.query(Clothing).filter(
            Clothing.id.in_(data['itemIds']),
            Clothing.user_id == user_id
        ).all()

        if len(clothes) != len(data['itemIds']):
            return jsonify({'error': '部分衣物不存在或无权访问'}), 400

        # Create outfit
        new_outfit = Outfit(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=data['name'],
            style=data.get('style', ''),
            occasion=data.get('occasion'),
            season=data.get('season'),
            ai_generated=True,
            reasoning=data.get('reasoning'),
            tips=json_dumps(data.get('tips', []))
        )

        db.session.add(new_outfit)
        db.session.flush()

        # Create outfit items
        for clothing_id in data['itemIds']:
            outfit_item = OutfitItem(
                id=str(uuid.uuid4()),
                outfit_id=new_outfit.id,
                clothing_id=clothing_id
            )
            db.session.add(outfit_item)

        db.session.commit()

        return jsonify(_outfit_to_dict(new_outfit, include_items=True)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'保存搭配失败: {str(e)}'}), 500
