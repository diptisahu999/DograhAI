"""Exotel telephony configuration schemas."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ExotelConfigurationRequest(BaseModel):
    """Request schema for Exotel configuration."""

    provider: Literal["exotel"] = Field(default="exotel")
    account_sid: str = Field(..., description="Exotel Account SID")
    account_region: Optional[str] = Field(default=None, description="Exotel Account region")
    subdomain: str = Field(default="api.exotel.com", description="Exotel Subdomain")
    api_key: str = Field(..., description="Exotel API Key (Username)")
    api_token: str = Field(..., description="Exotel API Token (Password)")
    from_numbers: List[str] = Field(
        default_factory=list, description="List of Exotel phone numbers"
    )


class ExotelConfigurationResponse(BaseModel):
    """Response schema for Exotel configuration with masked sensitive fields."""

    provider: Literal["exotel"] = Field(default="exotel")
    account_sid: str
    account_region: Optional[str] = None
    subdomain: str
    api_key: str
    api_token: str  # Masked
    from_numbers: List[str]
