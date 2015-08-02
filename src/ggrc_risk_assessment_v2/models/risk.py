# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from sqlalchemy.ext.declarative import declared_attr

from ggrc import db
from ggrc.models.associationproxy import association_proxy
from ggrc.models.object_owner import Ownable
from ggrc.models.object_document import Documentable
from ggrc.models.mixins import CustomAttributable, Base, Described, Slugged, Titled, WithContact, deferred, Stateful, Timeboxed
from ggrc.models.reflection import PublishOnly
from ggrc.models.relationship import Relatable


class Risk(CustomAttributable, Stateful, Relatable, Documentable, Described,
    Ownable, WithContact, Titled, Timeboxed, Slugged, Base, db.Model):
  __tablename__ = 'risks'

  VALID_STATES = [
      'Draft',
      'Final',
      'Effective',
      'Ineffective',
      'Launched',
      'Not Launched',
      'In Scope',
      'Not in Scope',
      'Deprecated',
      ]

  # Overriding mixin to make mandatory
  @declared_attr
  def description(cls):
    return deferred(db.Column(db.Text, nullable=False), cls.__name__)

  risk_objects = db.relationship(
      'RiskObject', backref='risk', cascade='all, delete-orphan')
  objects = association_proxy(
      'risk_objects', 'object', 'RiskObject')

  _publish_attrs = [
      'risk_objects',
      PublishOnly('objects'),
      ]
