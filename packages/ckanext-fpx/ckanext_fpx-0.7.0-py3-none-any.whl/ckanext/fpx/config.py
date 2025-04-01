from __future__ import annotations

import ckan.plugins.toolkit as tk

URL_LEGACY = "ckanext.fpx.service.url"
URL = "fpx.service.url"
INTERNAL_URL = "fpx.service.internal_url"
NO_QUEUE = "fpx.service.no_queue"

SECRET = "fpx.client.secret"
NAME = "fpx.client.name"


def url() -> str:
    return tk.config[URL]


def internal_url() -> str:
    return tk.config[INTERNAL_URL]


def no_queue() -> bool:
    return tk.config[NO_QUEUE]


def secret() -> str:
    return tk.config[SECRET]


def name() -> str:
    return tk.config[NAME]
