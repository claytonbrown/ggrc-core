# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for the mixin WithMigrationFlag."""
import collections

import ddt

from ggrc.converters import errors
from integration import ggrc
from integration.ggrc.models import factories


@ddt.ddt
class TestWithMigrationFlag(ggrc.TestCase):
  """Tests mixin WithMigrationFlag."""

  def setUp(self):
    super(TestWithMigrationFlag, self).setUp()
    self.api = ggrc.Api()

  @ddt.data(
      "Access Group",
      "Account Balance",
      "Data Asset",
      "Facility",
      "Key Report",
      "Market",
      "Metric",
      "Org Group",
      "Product",
      "Product Group",
      "Project",
      "Regulation",
      "Standard",
      "System",
      "Technology Environment",
      "Vendor",
      "Objective",
      "Requirement",
      "Threat",
      "Contract",
      "Policy",
  )
  def test_create_objects(self, obj_type):
    """Tests create objects without migration flag."""
    model_class = "".join(obj_type.split())
    factory = factories.get_model_factory(model_class)
    instance = factory(title="Object Title")
    res = instance.__class__.query.get(instance.id)
    self.assertEqual(res.migrate, False)

  @ddt.data(
      "Access Group",
      "Account Balance",
      "Data Asset",
      "Facility",
      "Key Report",
      "Market",
      "Metric",
      "Org Group",
      "Product",
      "Product Group",
      "Project",
      "Regulation",
      "Standard",
      "System",
      "Technology Environment",
      "Vendor",
      "Objective",
      "Requirement",
      "Threat",
      "Contract",
      "Policy",
  )
  def test_update_objects(self, obj_type):
    """Tests update objects with migrate flag."""
    model_class = "".join(obj_type.split())
    factory = factories.get_model_factory(model_class)
    instance = factory(title="Object Title")
    resp = self.api.put(instance, {"migrate": True})
    self.assertEqual(resp.status_code, 200)
    res = instance.__class__.query.get(instance.id)
    self.assertEqual(res.migrate, True)

  @ddt.data(
      "Access Group",
      "Account Balance",
      "Data Asset",
      "Facility",
      "Key Report",
      "Market",
      "Metric",
      "Org Group",
      "Product",
      "Product Group",
      "Project",
      "Regulation",
      "Standard",
      "System",
      "Technology Environment",
      "Vendor",
      "Objective",
      "Requirement",
      "Threat",
      "Contract",
      "Policy",
  )
  def test_import_objects(self, obj_type):
    """Tests import objects with migrate flag."""
    model_class = "".join(obj_type.split())
    factory = factories.get_model_factory(model_class)
    instance = factory(title="Object Title")
    response = self.import_data(collections.OrderedDict([
        ("object_type", model_class),
        ("Code*", instance.slug),
        ("migrate", True),
    ]))
    self._check_csv_response(response, {
        obj_type: {
            "row_warnings": {
                errors.READONLY_WILL_BE_IGNORED.format(
                    line=3,
                    column_name="Migrate"
                )
            }
        }
    })
