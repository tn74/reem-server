from django.contrib import admin

# Register your models here.
from jsoneditor.fields.django_extensions_jsonfield import JSONField
from jsoneditor.forms import JSONEditor
from .models import TestModel


class TestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField:{ 'widget':JSONEditor },
    }
admin.site.register(TestModel, TestAdmin)
