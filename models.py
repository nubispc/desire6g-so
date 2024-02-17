from pydantic import BaseModel
from typing import List, Dict

class TodoItem(BaseModel):
    name: str
    description: str
    internal_connections: List[Dict]
    external_connections: List[Dict]
    VNFC: List[Dict]
