from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.database import supabase
from app.config import BASE_URL
from app.models import ShortenRequest, ShortenResponse
from app.utils import generate_alias, compute_expiry

router = APIRouter()
MAX_RETRIES = 5


def alias_exists(alias: str) -> bool:
    result = supabase.table("links").select("alias").eq("alias", alias).execute()
    return bool(result.data)


@router.post("/shorten", response_model=ShortenResponse, status_code=201)
async def shorten_url(body: ShortenRequest):
    is_custom = body.custom_alias is not None
    domain = None
    alias = body.custom_alias

    # ── Resolve alias & domain ──────────────────────────────────────
    if is_custom:
        # Handle the special format: __DOMAINED__|domain|alias
        if alias.startswith("__DOMAINED__|"):
            _, domain, alias = alias.split("|")
        
        if alias_exists(alias):
            raise HTTPException(
                status_code=409,
                detail=f"The alias '{alias}' is already taken. Please choose another.",
            )
    else:
        for _ in range(MAX_RETRIES):
            alias = generate_alias()
            if not alias_exists(alias):
                break
        else:
            raise HTTPException(
                status_code=500,
                detail="Could not generate a unique alias. Please try again.",
            )

    # ── Compute optional expiry ────────────────────────────────────
    expires_at = compute_expiry(body.expires_in_days)

    # ── Persist to Supabase ────────────────────────────────────────
    insert_result = supabase.table("links").insert({
        "alias": alias,
        "original_url": str(body.original_url),
        "is_custom": is_custom,
        "domain": domain,
        "expires_at": expires_at.isoformat() if expires_at else None,
    }).execute()

    if not insert_result.data:
        raise HTTPException(status_code=500, detail="Failed to save the link. Please try again.")

    # Return the localhost clickable link for testing,
    # AND show them what their custom domain URL will look like.
    return ShortenResponse(
        short_url=f"{BASE_URL}/{alias}",
        custom_domain_url=f"https://{domain}/{alias}" if domain else None,
        alias=alias,
        original_url=str(body.original_url),
        is_custom=is_custom,
        expires_at=expires_at,
        created_at=datetime.fromisoformat(insert_result.data[0]["created_at"]),
    )