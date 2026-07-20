"""create extracted documents table

Revision ID: 76ac4c647b9c
Revises: e3074d47147e
Create Date: 2026-07-13 01:00:02.705115

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76ac4c647b9c'
down_revision: Union[str, Sequence[str], None] = 'e3074d47147e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'extracted_documents',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'document_group_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'doc_type',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'extracted_data',
            sa.JSON(),
            nullable=False
        ),

        sa.Column(
            'confidence',
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            'extraction_source',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['document_group_id'],
            ['document_groups.id']
        ),

        sa.PrimaryKeyConstraint(
            'id'
        )
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table(
        'extracted_documents'
    )