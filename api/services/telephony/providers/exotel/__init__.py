"""Exotel telephony provider package."""

import uuid
from typing import Any, Dict

import aiohttp
from fastapi import HTTPException
from loguru import logger

from api.services.telephony.registry import (
    ProviderSpec,
    ProviderUIField,
    ProviderUIMetadata,
    register,
)
from api.utils.common import get_backend_endpoints

from .config import ExotelConfigurationRequest, ExotelConfigurationResponse
from .provider import ExotelProvider
from .transport import create_transport

EXOTEL_API_BASE_URL = "https://api.exotel.com/v1"


def _config_loader(value: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "provider": "exotel",
        "account_sid": value.get("account_sid"),
        "account_region": value.get("account_region"),
        "subdomain": value.get("subdomain"),
        "api_key": value.get("api_key"),
        "api_token": value.get("api_token"),
        "from_numbers": value.get("from_numbers", []),
    }


_UI_METADATA = ProviderUIMetadata(
    display_name="Exotel",
    docs_url="https://docs.dograh.com/integrations/telephony/exotel",
    fields=[
        ProviderUIField(name="account_sid", label="Account SID", type="text", sensitive=False),
        ProviderUIField(name="account_region", label="Account Region", type="text", required=False, sensitive=False, placeholder="e.g. Singapore"),
        ProviderUIField(name="subdomain", label="Subdomain", type="text", sensitive=False, placeholder="api.exotel.com"),
        ProviderUIField(name="api_key", label="API Key (Username)", type="text", sensitive=False),
        ProviderUIField(
            name="api_token", label="API Token (Password)", type="password", sensitive=True
        ),
        ProviderUIField(
            name="from_numbers",
            label="Phone Numbers",
            type="string-array",
            description="E.164-formatted Exotel phone numbers used for outbound calls",
        ),
    ],
)


SPEC = ProviderSpec(
    name="exotel",
    provider_cls=ExotelProvider,
    config_loader=_config_loader,
    transport_factory=create_transport,
    transport_sample_rate=8000,
    config_request_cls=ExotelConfigurationRequest,
    ui_metadata=_UI_METADATA,
    config_response_cls=ExotelConfigurationResponse,
    account_id_credential_field="account_sid",
)


register(SPEC)


__all__ = [
    "SPEC",
    "ExotelConfigurationRequest",
    "ExotelConfigurationResponse",
    "ExotelProvider",
    "create_transport",
]
