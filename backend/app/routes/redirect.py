from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.database import supabase
from app.utils import is_expired

router = APIRouter()


@router.get("/{alias}")
async def redirect_to_url(alias: str):
    # Aggressively ignore common static file requests and development assets
    # so they don't trigger a 404 from our database logic.
    alias_lower = alias.lower().strip("/")
    
    # 1. Exact matches for common root files and API prefix
    if alias_lower.startswith("api/") or alias_lower in ["api", "favicon.ico", "favicon.png", "apple-touch-icon.png", "index.html", "manifest.json", "robots.txt", "vite.svg"]:
        raise HTTPException(status_code=404)
    
    # 2. Check for any path with an extension (assets usually have dots)
    if "." in alias_lower:
        ext = alias_lower.split(".")[-1]
        if ext in ["png", "jpg", "jpeg", "gif", "svg", "css", "js", "map", "ico", "json", "txt"]:
            raise HTTPException(status_code=404)

    # 3. Handle health checks if hit here
    if alias_lower in ["health", "api/health"]:
        return {"status": "ok"}

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