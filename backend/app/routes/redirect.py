from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.database import supabase
from app.utils import is_expired

router = APIRouter()


@router.get("/{alias}")
async def redirect_to_url(alias: str):
    # Safely ignore common static file requests and development assets
    # so they don't trigger a 404 from the database logic.
    if alias in ["favicon.ico", "favicon.png", "index.html", "manifest.json", "robots.txt"]:
        raise HTTPException(status_code=404)
    
    if "." in alias:
        ext = alias.split(".")[-1].lower()
        if ext in ["png", "jpg", "jpeg", "gif", "svg", "css", "js", "map", "ico"]:
            raise HTTPException(status_code=404)

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