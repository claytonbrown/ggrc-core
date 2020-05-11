# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for the mixin WithMigrationFlag."""

import ddt

from ggrc.models import all_models
from integration import ggrc
from integration.ggrc import generator


@ddt.ddt
class TestWithMigrationFlag(ggrc.TestCase):
  """Tests mixin WithMigrationFlag."""

  def setUp(self):
    super(TestWithMigrationFlag, self).setUp()
    self.api = ggrc.Api()
    self.object_generator = generator.ObjectGenerator()
    self.objs = []

  @ddt.data(
      all_models.AccessGroup,
      all_models.AccountBalance,
      all_models.DataAsset,
      all_models.Facility,
      all_models.KeyReport,
      all_models.Market,
      all_models.Metric,
      all_models.OrgGroup,
      all_models.Process,
      all_models.Product,
      all_models.ProductGroup,
      all_models.Project,
      all_models.Regulation,
      all_models.Standard,
      all_models.System,
      all_models.TechnologyEnvironment,
      all_models.Vendor,
      all_models.Objective,
      all_models.Requirement,
      all_models.Threat,
      all_models.Contract,
      all_models.Policy
  )
  def test_create_objects(self, model_class):
    """Tests create objects without migration flag."""
    data = {"title": "Object Title"}
    response, obj = self.object_generator.generate_object(
        model_class,
        data=data
    )
    self.assertEqual(response.status_code, 201)
    self.objs.append((model_class, obj.id))
    res = model_class.query.get(obj.id)
    self.assertEqual(res.migrate, False)

  @ddt.data(
      all_models.AccessGroup,
      all_models.AccountBalance,
      all_models.DataAsset,
      all_models.Facility,
      all_models.KeyReport,
      all_models.Market,
      all_models.Metric,
      all_models.OrgGroup,
      all_models.Process,
      all_models.Product,
      all_models.ProductGroup,
      all_models.Project,
      all_models.Regulation,
      all_models.Standard,
      all_models.System,
      all_models.TechnologyEnvironment,
      all_models.Vendor,
      all_models.Objective,
      all_models.Requirement,
      all_models.Threat,
      all_models.Contract,
      all_models.Policy
  )
  def test_create_objects_flag_false(self, model_class):
    """Tests create objects with migrate flag is True."""
    data = {"title": "Object Title",
            "migrate": True}
    response, obj = self.object_generator.generate_object(
        model_class,
        data=data
    )
    self.assertEqual(response.status_code, 201)
    res = model_class.query.get(obj.id)
    self.assertEqual(res.migrate, False)

  def test_update_objects(self):
    """Tests update objects with migrate flag."""
    for model_class, obj_id in self.objs:
      obj = model_class.query.get(obj_id)
      resp = self.api.put(obj, {"migrate": True})
      self.assertEqual(resp.status_code, 200)
      res = model_class.query.get(obj.id)
      self.assertEqual(res.migrate, True)
