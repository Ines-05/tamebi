from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
from datetime import datetime
import re

ALIAS_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,30}$')


class ShortenRequest(BaseModel):
    original_url: str  # Use str to be less strict than HttpUrl
    custom_alias: Optional[str] = None
    expires_in_days: Optional[int] = None

    @field_validator("custom_alias")
    @classmethod
    def validate_alias(cls, v: Optional[str]):
        if v is None:
            return v
        
        # Normalize: remove http/https if present for easier parsing
        clean_v = v.replace("https://", "").replace("http://", "")
        
        # If user provides a full link (e.g., aprenx.com/c), extract parts
        if "/" in clean_v:
            # Strip query params and fragments
            clean_p = clean_v.split("?")[0].split("#")[0]
            parts = [p for p in clean_p.split("/") if p]
            
            if len(parts) >= 2:
                # First part is domain, last part is alias
                alias = parts[-1]
                domain = parts[0]
                
                if not ALIAS_PATTERN.match(alias):
                    raise ValueError("Alias part must be 3–30 alphanumeric characters")
                
                # Use | as a safer separator than : (in case of ports)
                return f"__DOMAINED__|{domain}|{alias.lower()}"
        
        # Simple alias case
        if not ALIAS_PATTERN.match(v):
            raise ValueError(
                "Alias must be 3–30 characters: letters, numbers, hyphens (-) or underscores (_) only"
            )
        return v.lower()

    @field_validator("expires_in_days")
    @classmethod
    def validate_expiry(cls, v):
        if v is not None and (v < 1 or v > 365):
            raise ValueError("Expiry must be between 1 and 365 days")
        return v


class ShortenResponse(BaseModel):
    short_url: str                # The clickable test link (localhost)
    custom_domain_url: Optional[str] = None  # The intended custom link (aprenx.com/c)
    alias: str
    original_url: str
    is_custom: bool
    expires_at: Optional[datetime] = None
    created_at: datetime


class AnalyticsResponse(BaseModel):
    alias: str
    original_url: str
    click_count: int
    is_custom: bool
    created_at: datetime
    expires_at: Optional[datetime] = None