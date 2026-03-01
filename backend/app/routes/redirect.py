from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.database import supabase
from app.utils import is_expired

router = APIRouter()


@router.get("/{alias}")
async def redirect_to_url(alias: str):
    result = supabase.table("links").select("*").eq("alias", alias).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail=f"No link found for alias '{alias}'")

    link = result.data[0]

    if is_expired(link.get("expires_at")):
        raise HTTPException(status_code=410, detail="This short link has expired.")

    # Increment click count (best-effort — won't block the redirect)
    try:
        supabase.table("links") \
            .update({"click_count": link["click_count"] + 1}) \
            .eq("alias", alias) \
            .execute()
    except Exception:
        pass

    return RedirectResponse(url=link["original_url"], status_code=301)