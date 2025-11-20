backend/
  api/
    routes.py
    routes_bindings.py

# backend/api/routes.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "OK"}

@router.get("/state/
    global_state.py
    config_loader.py