from dataclasses import dataclass , asdict 
from datetime import datetime 
from typing import Dict , Any , Optional 
@dataclass 
class QueryInfo :
    query_id : str 
    database:str 
    collection :str 
    operation : str# type de operation find , select, update ,delete 
    duration_ms:int 
    time :datetime
    status : str
    user : str 
    query_details : Optional[str] = None 
    def to_dict(self)-> Dict[str, Any]:
        data = asdict(self)
        data['time']=self.time.isoformat()
        return data 
    @classmethod
    def from_dict(cls, data:Dict[str , Any])->QueryInfo :
        if isinstance(data['time'], str):
            data['time']=datetime.fromisoformat(data['time'])
            return cls(**data)
    def is_slow_query(self ) -> bool :
        return self.duration_ms>100 
    def get_formatted_duration (self) -> str :
        if self.duration_ms < 1000 :
            return f"{self.duration_ms}ms"
        else :
            return f"{self.duration_ms / 1000:.2f}s"
