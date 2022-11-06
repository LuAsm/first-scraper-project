from pydantic import BaseModel
from typing import Optional

class Equipment(BaseModel):
    model : str
    main_equipment_image : Optional[str] 
    about_equipment : str
    price : str
    spec: str
    

class EquipmentLink(BaseModel):
    url: str