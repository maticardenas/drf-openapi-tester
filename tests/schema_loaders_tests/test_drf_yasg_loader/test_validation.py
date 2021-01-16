import pytest
from django.core.exceptions import ImproperlyConfigured

from openapi_tester.loaders import DrfYasgSchemaLoader


def test_drf_yasg_not_in_installed_apps(monkeypatch):
    """
    Verify that validation raises an exception if the package is not installed.
    """

    monkeypatch.setattr('django.conf.settings.INSTALLED_APPS', [])

    with pytest.raises(ImproperlyConfigured, match='is missing from INSTALLED_APPS'):
        DrfYasgSchemaLoader()