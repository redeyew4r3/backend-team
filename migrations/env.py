import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

config = context.config
fileConfig(config.config_file_name)

from models import Base

target_metadata = Base.metadata
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))

def run_migrations_online():
    connectable = engine_from_config(
        config.get_config(),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transaction_per_migration=True,
            version_table='alembic_version',
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    context.run_migrations()
else:
    run_migrations_online()