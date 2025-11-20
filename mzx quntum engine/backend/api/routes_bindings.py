# backend/api/routes_bindings.py — UPDATE
# (extend existing file)
from backend.integration.settings_binding import bind_settings

@router.post("/settings/update")
async def route_update_settings(data: dict):
    return await bind_settings(data)