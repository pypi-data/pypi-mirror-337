from typing import Dict, Optional, List, Any

from pydantic import BaseModel


class V1UserProfile(BaseModel):
    email: str
    display_name: Optional[str] = None
    handle: Optional[str] = None
    picture: Optional[str] = None
    organization: Optional[str] = None
    subscription: Optional[str] = None
    external_id: Optional[str] = None
    role: Optional[str] = None
    actor: Optional[str] = None
    organizations: Optional[Dict[str, Dict[str, Any]]] = None
    created: Optional[int] = None
    updated: Optional[int] = None
    token: Optional[str] = None
    entitlements: Optional[List[Dict[str, Any]]] = None