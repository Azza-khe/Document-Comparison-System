"""create extraction tables

Revision ID: 272ec0a48c99
Revises: 76ac4c647b9c
Create Date: 2026-07-15 11:37:28.752601

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '272ec0a48c99'
down_revision: Union[str, Sequence[str], None] = '76ac4c647b9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'extracted_items',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'document_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'line_number',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'product_code',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'description',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'quantity',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'unit',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'unit_price',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'discount',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'vat',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'total',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'confidence',
            sa.Float(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ['document_id'],
            ['extracted_documents.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )


    # Ajouter le statut d'extraction
    # avec valeur par défaut pour les anciennes lignes
    op.add_column(
        'extracted_documents',
        sa.Column(
            'extraction_status',
            sa.String(),
            nullable=False,
            server_default="PENDING"
        )
    )


    # Supprimer le server_default après migration
    op.alter_column(
        'extracted_documents',
        'extraction_status',
        server_default=None
    )


    # Un document group correspond à un seul document extrait
    op.create_unique_constraint(
        'uq_extracted_documents_group_id',
        'extracted_documents',
        ['document_group_id']
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'uq_extracted_documents_group_id',
        'extracted_documents',
        type_='unique'
    )

    op.drop_column(
        'extracted_documents',
        'extraction_status'
    )

    op.drop_table(
        'extracted_items'
    )