# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
create_banner_table

Create Date: 2020-05-07 13:24:27.044567
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

from ggrc.models import all_models


# revision identifiers, used by Alembic.
revision = 'b8a0d301eb50'
down_revision = 'e3577a2b4e03'

default_data = all_models.Banner.DEFAULT_BANNER_DATA


def create_default_banner(conn, default_data):
  """Function that create default banner in database
  Args:
    conn: Database connection
    default_data: Dict() with default data values
  """

  query = sa.text(
    """
        INSERT INTO banner (message, bg_color, font_color)
        VALUES (:msg, :bg_clr, :font_clr)
    """
  )

  conn.execute(
      query,
      msg=default_data["message"],
      bg_clr=default_data["bg_color"],
      font_clr=default_data["font_color"]
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  conn = op.get_bind()

  op.create_table(
      'banner',
      sa.Column('message', sa.Text()),
      sa.Column('bg_color', sa.String(length=10)),
      sa.Column('font_color', sa.String(length=10)),
  )

  create_default_banner(conn, default_data)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
