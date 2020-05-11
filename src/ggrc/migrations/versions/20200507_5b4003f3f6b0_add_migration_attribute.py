# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add Migration Attribute

Create Date: 2020-05-07 17:05:29.223532
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op, context

# revision identifiers, used by Alembic.

revision = '5b4003f3f6b0'
down_revision = 'b8a0d301eb50'

tables_list = [
    "access_groups",
    "account_balances",
    "data_assets",
    "facilities",
    "key_reports",
    "markets",
    "metrics",
    "org_groups",
    "products",
    "product_groups",
    "projects",
    "systems",
    "technology_environments",
    "vendors",
    "directives",
    "objectives",
    "requirements",
    "threats",
]


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  with context.begin_transaction():
    for table in tables_list:
      op.add_column(
          table,
          sa.Column("migrate", sa.Boolean, default=False, nullable=False),
      )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
