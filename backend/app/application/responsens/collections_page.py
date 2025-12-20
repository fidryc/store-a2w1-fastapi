from pydantic import BaseModel
from app.schemas.dto import CollectionDTO

class CollectionsByCatIdPageResponse(BaseModel):
    collections: list[CollectionDTO] = None
    
class CollectionByIdPageResponse(BaseModel):
    collections: list[CollectionDTO] = None