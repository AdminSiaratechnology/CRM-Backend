import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.permission import Permission, RolePermission
from app.models.role import Role
from app.models.tenant import Tenant


def seed_permissions():
    db = SessionLocal()
    try:
        # Define default permissions
        modules_with_actions = [
            ("users", ["view", "create", "edit", "delete"]),
            ("roles", ["view", "create", "edit", "delete", "manage_permissions"]),
            ("permissions", ["view", "create", "edit", "delete"]),
            ("hierarchy", ["view", "create", "edit", "delete"]),
            ("branches", ["view", "create", "edit", "delete"]),
            ("teams", ["view", "create", "edit", "delete"]),
            ("managers", ["view", "create", "edit", "delete"]),
            ("departments", ["view", "create", "edit", "delete"]),
            ("territories", ["view", "create", "edit", "delete"]),
            ("custom_fields", ["view", "create", "edit", "delete"]),
            ("form_builder", ["view", "create", "edit", "delete"]),
            ("master_data", ["view", "create", "edit", "delete"]),
            ("audit_logs", ["view"]),
            ("leads", ["view", "create", "edit", "delete", "assign", "convert"]),
            ("deals", ["view", "create", "edit", "delete", "approve"]),
            ("finance", ["view", "create", "edit", "delete", "payment"]),
            ("support", ["view", "create", "edit", "delete", "resolve"]),
            ("communication", ["send"]),
            ("marketing", ["manage"]),
            ("reports", ["view"]),
            ("admin", ["manage"]),
            ("aiCommand", ["view", "manage"]),
        ]
        
        # Get the first tenant (or create one if doesn't exist)
        tenant = db.query(Tenant).first()
        if not tenant:
            print("No tenant found. Please create a tenant first.")
            return
        
        tenant_id = tenant.id
        
        # Create permissions
        permission_map = {}  # name -> Permission object
        for module, actions in modules_with_actions:
            for action in actions:
                name = f"{module}.{action}"
                
                # Check if permission already exists
                existing = db.query(Permission).filter(
                    Permission.tenant_id == tenant_id,
                    Permission.name == name
                ).first()
                
                if existing:
                    permission_map[name] = existing
                    continue
                
                perm = Permission(
                    tenant_id=tenant_id,
                    code=name,
                    label=name.replace(".", " ").title(),
                    module=module,
                    action=action,
                    name=name,
                    description=f"Permission to {action} {module}",
                    status="active"
                )
                db.add(perm)
                db.flush()
                permission_map[name] = perm
        
        db.commit()
        
        # Get or create Admin role
        admin_role = db.query(Role).filter(
            Role.tenant_id == tenant_id,
            Role.code == "admin"
        ).first()
        
        if not admin_role:
            admin_role = Role(
                tenant_id=tenant_id,
                name="Admin",
                code="admin",
                description="Administrator role with full access",
                status="active"
            )
            db.add(admin_role)
            db.flush()
        
        # Assign all permissions to Admin role
        # First delete existing role permissions for admin
        db.query(RolePermission).filter(
            RolePermission.tenant_id == tenant_id,
            RolePermission.role_id == admin_role.id
        ).delete()
        
        # Add all permissions
        for name, perm in permission_map.items():
            rp = RolePermission(
                tenant_id=tenant_id,
                role_id=admin_role.id,
                permission_id=perm.id
            )
            db.add(rp)
        
        db.commit()
        print("Seeding completed successfully!")
        print(f"Created {len(permission_map)} permissions")
        print(f"Assigned all permissions to Admin role")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding permissions: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_permissions()
