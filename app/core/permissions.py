ROLE_PERMISSIONS = {
    "Super Admin": {"*"},
    "Company Owner": {"leads.view", "leads.create", "leads.edit", "leads.delete", "leads.assign", "leads.convert", "deals.view", "deals.create", "deals.edit", "deals.delete", "deals.approve", "finance.view", "finance.create", "finance.edit", "finance.delete", "finance.payment", "support.view", "support.create", "support.edit", "support.delete", "support.resolve", "communication.send", "marketing.manage", "reports.view", "admin.manage", "aiCommand.view", "aiCommand.manage"},
}


def has_permission(role_name: str, permission: str) -> bool:
    allowed = ROLE_PERMISSIONS.get(role_name, set())
    return "*" in allowed or permission in allowed
