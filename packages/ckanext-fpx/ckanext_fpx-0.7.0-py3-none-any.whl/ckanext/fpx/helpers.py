from __future__ import annotations

import os
import logging

from typing import Optional

import jwt

from ckan.exceptions import CkanConfigurationException

import ckan.plugins.toolkit as tk
from . import utils, config

log = logging.getLogger(__name__)


def get_helpers():
    return {
        "fpx_service_url": fpx_service_url,
        "fpx_into_stream_url": fpx_into_stream_url,
        "fpx_no_queue": fpx_no_queue,
    }


def fpx_no_queue() -> bool:
    """Start downloads immediately, without waiting in queue.

    Requires FPX service running with `FPX_NO_QUEUE = True` option(default from
    v0.4.0).

    """
    return config.no_queue()


def fpx_service_url(*, internal: bool = False) -> str:
    f"""Return the URL of FPX service.

    Keyword Args:

        internal(optional): make an attempt to return value of
        `{config.internal_url()}` option. This feature can be used internally(for
        ticket ordering) in order to bypass load-balancer and access FPX
        service directly. When `{config.internal_url()}` is empty, normal
        URL(`{config.url()}`) is returned instead.

    """
    url = config.url()

    if internal:
        internal_url = config.internal_url()
        if internal_url:
            log.debug("Switching to internal URL")
            url = internal_url

    return url.rstrip("/") + "/"


def fpx_into_stream_url(url: str) -> Optional[str]:
    """Turn arbitrary link into URL to downloadable stream.

    In this way any URL that is accessible only from FPX service can be proxied
    to the client through FPX.

    Args:
        url: Download URL

    Returns:
        URL to the FPX endpoint that streams content from the Download URL.
        None, if client's name or secret are missing.

    """
    name = utils.client_name()
    secret = utils.client_secret()

    if not name or not secret:
        log.debug(
            "Do not generate stream URL because client details are incomplete"
        )
        return

    filename = os.path.basename(url.rstrip("/"))
    encoded = jwt.encode(
        {
            "url": url,
            "response_headers": {
                "content-disposition": f'attachment; filename="{filename}"'
            },
        },
        secret,
        algorithm="HS256",
    ).decode("utf8")
    service = tk.h.fpx_service_url()
    url = f"{service}stream/url/{encoded}?client={name}"

    return url
