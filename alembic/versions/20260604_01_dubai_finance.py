"""add dubai finance tables

Revision ID: 20260604_01_dubai_finance
Revises:
Create Date: 2026-06-04
"""

from alembic import op
import sqlalchemy as sa


revision = "20260604_01_dubai_finance"
down_revision = None
branch_labels = None
depends_on = None


COMMON_COLUMNS = [
    sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
    sa.Column("tenant_id", sa.String(length=36), nullable=False),
    sa.Column("branch_id", sa.String(length=36), nullable=True),
    sa.Column("team_id", sa.String(length=36), nullable=True),
    sa.Column("owner_id", sa.String(length=36), nullable=True),
    sa.Column("created_by_id", sa.String(length=36), nullable=True),
    sa.Column("updated_by_id", sa.String(length=36), nullable=True),
    sa.Column("status", sa.String(length=80), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
]


def _indexes(table_name: str, extra: list[str]) -> None:
    op.create_index(f"ix_{table_name}_tenant_id", table_name, ["tenant_id"])
    op.create_index(f"ix_{table_name}_branch_id", table_name, ["branch_id"])
    op.create_index(f"ix_{table_name}_team_id", table_name, ["team_id"])
    op.create_index(f"ix_{table_name}_owner_id", table_name, ["owner_id"])
    op.create_index(f"ix_{table_name}_status", table_name, ["status"])
    op.create_index(f"ix_{table_name}_created_at", table_name, ["created_at"])
    for column in extra:
        op.create_index(f"ix_{table_name}_{column}", table_name, [column])


def upgrade() -> None:
    op.create_table(
        "dubai_finance_applications",
        *COMMON_COLUMNS,
        sa.Column("application_number", sa.String(length=120), nullable=False),
        sa.Column("applicant_name", sa.String(length=255), nullable=False),
        sa.Column("applicant_mobile", sa.String(length=30), nullable=True),
        sa.Column("applicant_email", sa.String(length=255), nullable=True),
        sa.Column("employment_type", sa.String(length=80), nullable=True),
        sa.Column("bank_name", sa.String(length=120), nullable=True),
        sa.Column("stage", sa.String(length=100), nullable=False),
        sa.Column("required_amount", sa.Float(), nullable=True),
        sa.Column("approved_amount", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    _indexes("dubai_finance_applications", ["application_number", "applicant_email", "applicant_mobile", "stage"])
    op.create_index("ix_dubai_finance_applications_tenant_application", "dubai_finance_applications", ["tenant_id", "application_number"], unique=True)

    op.create_table(
        "dubai_finance_applicants",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("mobile", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("nationality", sa.String(length=120), nullable=True),
    )
    _indexes("dubai_finance_applicants", ["application_id", "email", "mobile"])

    op.create_table(
        "dubai_finance_employments",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("employer_name", sa.String(length=255), nullable=True),
        sa.Column("designation", sa.String(length=120), nullable=True),
        sa.Column("monthly_income", sa.Float(), nullable=True),
    )
    _indexes("dubai_finance_employments", ["application_id"])

    op.create_table(
        "dubai_finance_requirements",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("requirement_type", sa.String(length=120), nullable=True),
        sa.Column("property_value", sa.Float(), nullable=True),
        sa.Column("requested_amount", sa.Float(), nullable=True),
        sa.Column("tenure_months", sa.Integer(), nullable=True),
    )
    _indexes("dubai_finance_requirements", ["application_id"])

    op.create_table(
        "dubai_finance_documents",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("document_type", sa.String(length=120), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_url", sa.String(length=1000), nullable=True),
    )
    _indexes("dubai_finance_documents", ["application_id", "document_type"])

    op.create_table(
        "dubai_finance_bank_selections",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("bank_name", sa.String(length=120), nullable=False),
        sa.Column("selected_by", sa.String(length=120), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
    )
    _indexes("dubai_finance_bank_selections", ["application_id", "bank_name"])

    op.create_table(
        "dubai_finance_bank_submissions",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("bank_name", sa.String(length=120), nullable=False),
        sa.Column("submission_reference", sa.String(length=120), nullable=True),
        sa.Column("bank_status", sa.String(length=120), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
    )
    _indexes("dubai_finance_bank_submissions", ["application_id", "bank_name", "submission_reference", "bank_status"])

    op.create_table(
        "dubai_finance_status_history",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("from_stage", sa.String(length=100), nullable=True),
        sa.Column("to_stage", sa.String(length=100), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
    )
    _indexes("dubai_finance_status_history", ["application_id", "to_stage"])

    op.create_table(
        "dubai_finance_approval_rejections",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("decision", sa.String(length=50), nullable=False),
        sa.Column("decided_by", sa.String(length=120), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
    )
    _indexes("dubai_finance_approval_rejections", ["application_id", "decision"])

    op.create_table(
        "dubai_finance_commissions",
        *COMMON_COLUMNS,
        sa.Column("application_id", sa.String(length=36), nullable=False),
        sa.Column("bank_name", sa.String(length=120), nullable=True),
        sa.Column("amount", sa.Float(), nullable=True),
        sa.Column("commission_status", sa.String(length=80), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
    )
    _indexes("dubai_finance_commissions", ["application_id", "bank_name", "commission_status"])


def downgrade() -> None:
    for table_name in [
        "dubai_finance_commissions",
        "dubai_finance_approval_rejections",
        "dubai_finance_status_history",
        "dubai_finance_bank_submissions",
        "dubai_finance_bank_selections",
        "dubai_finance_documents",
        "dubai_finance_requirements",
        "dubai_finance_employments",
        "dubai_finance_applicants",
        "dubai_finance_applications",
    ]:
        op.drop_table(table_name)
