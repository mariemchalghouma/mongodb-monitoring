from dataclasses import dataclass , sadict 
from datetime import datetime
from typing import Dict , Any 
from enum import Emun


class AlertType (Enum):
    CRITICAL ="Criticial"
    WARNING ="WArning"
    INFO ="Info"

class AlertCategory (Enum) :
    PERFORMANCE="Performance"
    CONNECTION="Connection"
    QUERY="Query"
    RESOURCE="Resource"
    SYSTEM="System"
@dataclass
class Alert :
    alert_type: str
    category : str 
    title : str 
    message : str 
    time : datetime
    acknowleged : bool=False 
    acknowleged_by :str=""
    acknowleged_at : datetime =None 
    severity_score:int=0 
    def to_dict(self)->Dict[str , Any] :
        data= asdict(self)
        data['time']=self.time.isoformat()
        if self.acknowleged_at:
            data['acknowleged_at']=self.acknowleged_at.isoformat()
        return data 
    @classmethod
    def from_dict (cls , data: Dict[str , Any]) -> 'Alert' :
        if isinstance(data['time'], str) :
            data['time']= self.time.fromisoformat(data['time'])
        if isinstance(data['acknowleged_at']):
            data['acknowleged_at'] =self.acknowleged_at.fromisoformat(data['acknowleged_at'])
        return cls(**data)
    
    def acknowleged(self , user: str= "system"):
        self.acknowleged= True
        self.acknowleged_by =user
        self.acknowleged_at =datetime.now()
    def get_age_minutes(self) -> int:
        
        return int((datetime.now() - self.time).total_seconds() / 60)
    



    

