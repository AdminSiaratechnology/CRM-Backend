from app.schemas.auth import CurrentUser


def scoped_filters(user: CurrentUser) -> dict:
    filters = {"tenant_id": user.tenant_id, "deleted_at": None}
    if user.scope == "BRANCH" and user.branch_id:
        filters["branch_id"] = user.branch_id
    if user.scope == "TEAM" and user.team_id:
        filters["team_id"] = user.team_id
    if user.scope == "OWN":
        filters["owner_id"] = user.user_id
    return filters
