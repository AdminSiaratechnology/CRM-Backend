# User Creation API - Complete Setup

## Endpoint
**POST** `/api/v1/admin/users`

## Required Permission
`admin.manage`

## Request Body (JSON)
```json
{
  "name": "Ahmed Khan",
  "email": "ahmed@example.com",
  "password": "securepassword123",
  "mobile": "971501234567",
  "role_id": "role-uuid-here",
  "branch_id": "branch-uuid-here",
  "manager_id": "manager-uuid-here",
  "status": "active",
  "login_access": true,
  "gps_access": false,
  "monthly_target": 50000
}
```

## Field Descriptions

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| name | string | ✅ Yes | - | User's full name (max 255 chars) |
| email | string | ✅ Yes | - | Unique email address (max 255 chars) |
| password | string | ✅ Yes | - | User's password (will be hashed) |
| mobile | string | ❌ No | null | Phone number (max 30 chars) |
| role_id | string (UUID) | ❌ No | null | Reference to the user's role |
| branch_id | string (UUID) | ❌ No | null | Reference to the user's branch |
| manager_id | string (UUID) | ❌ No | null | Reference to the user's manager |
| status | string | ❌ No | "active" | User status (active/inactive/etc) |
| login_access | boolean | ❌ No | true | Whether user can login |
| gps_access | boolean | ❌ No | false | Whether user has GPS tracking enabled |
| monthly_target | integer | ❌ No | null | User's monthly sales/performance target |

## Response (Success - 200)
```json
{
  "success": true,
  "message": "User created",
  "data": {
    "id": "265db9ee-654a-48e9-94bf-e8d9aced6128",
    "name": "Ahmed Khan",
    "email": "ahmed@example.com",
    "mobile": "971501234567",
    "role_id": "role-uuid",
    "branch_id": "branch-uuid",
    "manager_id": "manager-uuid",
    "status": "active",
    "login_access": true,
    "gps_access": false,
    "monthly_target": 50000,
    "tenant_id": "SYSTEM",
    "created_by_id": "current-user-id",
    "updated_by_id": "current-user-id",
    "created_at": "2026-06-18T10:30:00",
    "updated_at": "2026-06-18T10:30:00",
    "deleted_at": null
  },
  "meta": {}
}
```

## Error Responses

### Missing Password (400)
```json
{
  "success": false,
  "message": "Password is required",
  "error_code": "PASSWORD_REQUIRED",
  "details": {}
}
```

### Duplicate Email (400)
```json
{
  "success": false,
  "message": "Duplicate key value violates unique constraint",
  "error_code": "INTEGRITY_ERROR",
  "details": {}
}
```

## Files Updated

1. **Model** - `/app/models/user.py`
   - Added `branch_id` field
   - Added `manager_id` field
   - Added `login_access` field (default: True)
   - Added `gps_access` field (default: False)
   - Added `monthly_target` field

2. **Schema** - `/app/schemas/admin.py`
   - Created `AdminUserCreate` schema with all new fields
   - All fields except name, email, and password are optional

3. **Service** - `/app/services/admin_service.py`
   - Updated `create_user()` method to handle all fields
   - Added payload validation and cleaning
   - Proper password hashing and user creation workflow

4. **Endpoint** - `/app/api/v1/endpoints/admin.py`
   - POST `/users` endpoint already available
   - Automatically accepts all new fields

## API Usage Example (cURL)

```bash
curl -X POST http://localhost:8000/api/v1/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Ahmed Khan",
    "email": "ahmed@example.com",
    "password": "securepassword123",
    "mobile": "971501234567",
    "role_id": "role-123",
    "branch_id": "branch-456",
    "manager_id": "manager-789",
    "status": "active",
    "login_access": true,
    "gps_access": false,
    "monthly_target": 50000
  }'
```

## Features Implemented

✅ User creation with all required fields
✅ Email and mobile number validation
✅ Password hashing and security
✅ Branch assignment
✅ Manager assignment
✅ Role assignment
✅ Login access control
✅ GPS tracking access control
✅ Monthly sales target setting
✅ Tenant scope support
✅ Audit trail (created_by_id, updated_by_id)
✅ Error handling with meaningful messages
