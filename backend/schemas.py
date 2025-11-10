from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class Lead(BaseModel):
    car_reference: str = Field(..., description="Car ad link or model name provided by the user")
    phone: str = Field(..., min_length=7, max_length=20, description="Contact phone number")
    plan: Optional[str] = Field(default=None, description="Selected pricing plan")

# Collection name derived from class name: "lead"
