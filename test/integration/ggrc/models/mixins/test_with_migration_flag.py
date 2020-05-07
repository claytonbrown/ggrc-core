import ddt

from ggrc.models import all_models
from integration.ggrc import TestCase, Api
from integration.ggrc.generator import ObjectGenerator


@ddt.ddt
class TestWithMigrationFlag(TestCase):

  def setUp(self):
    super(TestWithMigrationFlag, self).setUp()
    self.api = Api()
    self.object_generator = ObjectGenerator()

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
    data = {"title": "Object Title"}
    response, obj = self.object_generator.generate_object(
        model_class,
        data=data
    )
    self.assertEqual(response.status_code, 201)
    result = model_class.query.get(obj.id)
    self.assertEqual(result.id, obj.id)
    self.assertEqual(result.title, obj.title)
    self.assertEqual(result.migrate, False)
    resp = self.api.put(obj, {"migrate": True})
    self.assertEqual(resp.status_code, 200)
    res = model_class.query.get(obj.id)
    self.assertEqual(res.migrate, True)
