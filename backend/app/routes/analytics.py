from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.models import AnalyticsResponse

router = APIRouter()


@router.get("/", response_model=list[AnalyticsResponse])
async def list_links(limit: int = 50, offset: int = 0):
    """List all links with pagination."""
    result = (
        supabase.table("links")
        .select("*")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return result.data


@router.get("/{alias}", response_model=AnalyticsResponse)
async def get_link_analytics(alias: str):
    result = supabase.table("links").select("*").eq("alias", alias).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail=f"No link found for alias '{alias}'")
    return result.data[0]


@router.delete("/{alias}", status_code=204)
async def delete_link(alias: str):
    result = supabase.table("links").select("alias").eq("alias", alias).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail=f"No link found for alias '{alias}'")
    supabase.table("links").delete().eq("alias", alias).execute()