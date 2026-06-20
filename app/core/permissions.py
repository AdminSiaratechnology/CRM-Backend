from app.schemas.auth import CurrentUser


def has_permission(user: CurrentUser, permission: str) -> bool:
    """Check if current user has a specific permission."""
    # Check if user is super admin or has wildcard permission
    if user.is_superuser or user.role_name == "Super Admin":
        return True
    
    # Check if permission exists in user's permissions
    return permission in user.permissions

