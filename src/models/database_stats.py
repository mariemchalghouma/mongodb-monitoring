import pymongo 
from dataclasses import dataclass , asdict 
from datetime import datetime 
from typing  import Dict , Any 
@dataclass
class DatabaseStats :
    connection_status: str 
    # etat de la connction connected ou disconnection , erreur 
    active_connection : int 
    # nbr de connexions actives
    available_connection : int 
    # nbr de connexions dans  le pool  
    current_queue : int 
    # nbr des requete dans la file d'attente 
    avg_response_time : float 
    # temps  de reponse moyen des requete 
    operation_per_seconde : float 
    # nbr des operation par seconde 
    memory_usage : float 
    #utilsation memoire de mongodn en MB
    cpu_usage: float 
    # % d'utilisation CPU du serveur 
    disque_usage : float 
    # % d'utilisation du disque 
    time : datetime
    def to_dict(self) -> Dict[str, Any]:
        data=asdict(self)
        data["time"]=self.time.isoformat()
        return data 
    @classmethod
    def from_dict(cls , data: Dict[str, Any]) ->'DatabaseStats' :
        if isinstance(data['time'], str):
            data['time'] =datetime.fromisoformat(data['time'])
        return cls(**data)
    
    def get_connection_percentage(self) -> float :
        total =self.active_connection + self.available_connection
        if total==0 :
            return 0.0 
        return (self.active_connection/total)*100





