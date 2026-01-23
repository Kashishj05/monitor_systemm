from pydantic import BaseModel
from datetime import datetime


class ActivityLogResponse(BaseModel):
    id:int
    actor_id:int
    action:str
    entity_type:str
    entity_id:int
    description :str|None
    created_at:datetime
   
    class Config:
        from_attributes=True


   