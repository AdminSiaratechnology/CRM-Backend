from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def write_audit_log(
    db: Session,
    *,
    tenant_id: str,
    actor_id: str | None,
    module: str,
    action: str,
    entity_id: str | None = None,
    before_data: dict | None = None,
    after_data: dict | None = None,
) -> None:
    db.add(
        AuditLog(
            tenant_id=tenant_id,
            actor_id=actor_id,
            module=module,
            action=action,
            entity_id=entity_id,
            before_data=before_data,
            after_data=after_data,
        )
    )
