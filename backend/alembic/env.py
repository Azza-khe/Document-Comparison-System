from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from dotenv import load_dotenv
import os


# =====================================================
# Charger les modèles SQLAlchemy
# =====================================================

from app.core.database import Base

from app.models.job import Job
from app.models.page import Page
from app.models.review_queue import ReviewQueue
from app.models.document_group import DocumentGroup
from app.models.document_group_page import DocumentGroupPage
from app.models.extracted_document import ExtractedDocument
from app.models.extracted_document import ExtractedDocument
from app.models.extracted_item import ExtractedItem


# =====================================================
# Charger .env
# =====================================================

load_dotenv()


# =====================================================
# Configuration Alembic
# =====================================================

config = context.config


config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)


# =====================================================
# Logging
# =====================================================

if config.config_file_name is not None:

    fileConfig(
        config.config_file_name
    )


# =====================================================
# Import obligatoire des modèles
# pour Alembic autogenerate
# =====================================================

import app.models.job
import app.models.page
import app.models.review_queue
import app.models.document_group
import app.models.document_group_page
import app.models.extracted_document
import app.models.extracted_document
import app.models.extracted_item


# Metadata utilisée par Alembic

target_metadata = Base.metadata



# =====================================================
# Migration OFFLINE
# =====================================================

def run_migrations_offline() -> None:


    url = config.get_main_option(
        "sqlalchemy.url"
    )


    context.configure(

        url=url,

        target_metadata=target_metadata,

        literal_binds=True,

        dialect_opts={
            "paramstyle": "named"
        },

    )


    with context.begin_transaction():

        context.run_migrations()



# =====================================================
# Migration ONLINE
# =====================================================

def run_migrations_online() -> None:


    connectable = engine_from_config(

        config.get_section(
            config.config_ini_section,
            {}
        ),

        prefix="sqlalchemy.",

        poolclass=pool.NullPool,

    )


    with connectable.connect() as connection:


        context.configure(

            connection=connection,

            target_metadata=target_metadata,

        )


        with context.begin_transaction():

            context.run_migrations()



# =====================================================
# Execution
# =====================================================

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()