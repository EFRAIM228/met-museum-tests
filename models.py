from typing import List, Optional
from pydantic import BaseModel

class ArtObject(BaseModel):
    objectID: int
    title: str
    artist: Optional[str] = None
    objectName: Optional[str] = None
    medium: Optional[str] = None
    culture: Optional[str] = None
    period: Optional[str] = None
    date: Optional[str] = None
    objectDate: Optional[str] = None
    dimensions: Optional[str] = None
    classification: Optional[str] = None
    department: Optional[str] = None
    isHighlight: bool
    hasImage: Optional[bool] = None
    primaryImage: Optional[str] = None
    primaryImageSmall: Optional[str] = None


class SearchResponse(BaseModel):
    total: int
    objectIDs: List[int]
    limit: Optional[int] = None      # <-- сделали необязательным
    offset: Optional[int] = None     # <-- сделали необязательным


class ObjectListResponse(BaseModel):
    objects: List[ArtObject]


