# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


from ggrc import db
from ggrc.models.mixins.base import Dictable
from ggrc.models.inflector import ModelInflectorDescriptor



class Banner(Dictable, db.Model):
  """Class for Alert banner"""

  __tablename__ = "banner"
  _inflector = ModelInflectorDescriptor()

  DEFAULT_BANNER_DATA = {
      "message": "This is default banner's notice",
      "bg_color": "31d018",
      "font_color": "FFFFFF"
  }

  message = db.Column(db.String, primary_key=True)
  font_color = db.Column(db.String(10))
  bg_color = db.Column(db.String(10))

