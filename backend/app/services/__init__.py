"""Business logic services for the OOTD application."""
from app.services.auth_service import (
    get_user_by_email,
    get_user_by_id,
    register_user,
    authenticate_user,
    create_user_token,
)
from app.services.user_service import (
    get_user,
    update_user_profile,
    get_all_users,
)
from app.services.wardrobe_service import (
    get_clothing_by_id,
    get_user_clothes,
    create_clothing,
    update_clothing,
    delete_clothing,
    get_clothing_categories,
)
from app.services.outfit_service import (
    get_outfit_by_id,
    get_user_outfits,
    create_outfit,
    update_outfit,
    delete_outfit,
    get_outfit_items,
    get_outfit_styles,
)
from app.services.tongyi_service import (
    ZhipuClothingItem,
    ZhipuUser,
    ZhipuRequirements,
    generate_outfit_recommendation,
)

__all__ = [
    "get_user_by_email",
    "get_user_by_id",
    "register_user",
    "authenticate_user",
    "create_user_token",
    "get_user",
    "update_user_profile",
    "get_all_users",
    "get_clothing_by_id",
    "get_user_clothes",
    "create_clothing",
    "update_clothing",
    "delete_clothing",
    "get_clothing_categories",
    "get_outfit_by_id",
    "get_user_outfits",
    "create_outfit",
    "update_outfit",
    "delete_outfit",
    "get_outfit_items",
    "get_outfit_styles",
    "ZhipuClothingItem",
    "ZhipuUser",
    "ZhipuRequirements",
    "generate_outfit_recommendation",
]
