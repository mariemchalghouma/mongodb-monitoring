from pymongo import MongoClient 
import psutil
 
import yaml
from datetime import datetime 
 
 


class MetricsCollector :
    def __init__(self, config_path):
        with open (config_path , 'r') as file :
            config= yaml.safe_load(file)
        self.config=config
        self.mongodb_uri=config['mongodb']['uri']
        self.db_name=config['mongodb']['database']
        self.client=MongoClient(self.mongodb_uri)

    def collect_cpu_usage(self):
        return psutil.cpu_percent(interval=1)
    def collect_memory_usage(self):
        return psutil.virtual_memory().percent
    def collect_disk_usage(self):
        return psutil.disk_usage('/').percent
    def collect_connection_count(self) :
        try:
            server_status=self.client[self.db_name].command("serverStatus")
            return server_status['connections']['current']
        except Exception as e :
            print("erreur ")
            return None 
    def collect_query_performance(self):
        try :
            server_status=self.client[self.db_name].command("serverStatus")
            return server_status["opcounters"]
        except Exception as e :
            return None 
    def collect_all (self):
        metrics={}
        for metric in self.config['monitoring']['metrics_to_collect']:
            if metric=="cpu_usage":
                metrics['cpu_usage']=self.collect_cpu_usage()
                print(metric)
            elif metric=="memory_usage" :
                metrics["memory_usage"]=self.collect_memory_usage()
                print(metric)
            elif metric=="disk_usage" :
                metrics['disk_usage']=self.collect_disk_usage()
                print(metric)
            elif metric=="connection_count":
                metrics['connection_count']=self.collect_connection_count()
                print(metric)
            elif metric=="query_performance" :
                metrics['query_performance']=self.collect_query_performance()
        metrics['time']=datetime.now().isoformat()
        print(metrics)
        return metrics
'''if __name__=="__main__" :
    try:
         
        collector= MetricsCollector("C:/Users/Admin/Desktop/mongodb_monitoring/config.yaml")
        metrics=collector.collect_all()
        print("Métriques collectées :")
    except Exception as e :
        print(f"Erreur lors de l'exécution : {e}")'''
    




        

    

    
