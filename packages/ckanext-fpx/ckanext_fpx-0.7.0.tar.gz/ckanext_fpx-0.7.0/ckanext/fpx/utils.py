import logging

from ckan.plugins import PluginImplementations
from . import interfaces, config

log = logging.getLogger(__name__)

CONFIG_SECRET_LEGACY = "ckanext.fpx.client.secret"
CONFIG_SECRET = "fpx.client.secret"

CONFIG_NAME = "fpx.client.name"


def client_secret():
    return config.secret()


def client_name():
    return config.name()


def get_normalizer() -> interfaces.IFpx:
    """Return normalizer for FPX payload.

    The first plugins that implements IFpx interface will be used as normalizer.
    """
    return next(iter(PluginImplementations(interfaces.IFpx)))
