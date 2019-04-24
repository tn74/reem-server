from django.db import models

# from json_field import JSONField replaced by:
from jsoneditor.fields.django_json_field import JSONField
# Create your models here.

class TestModel(models.Model):
    my_field = JSONField()