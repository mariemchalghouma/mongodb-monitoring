import logging 
from datetime import datetime , timedelta 
from typing import Dict ,List , Any , Optional 
from pymongo import MongoClient 
from pymongo.errors import OperationFailure 

class IndexAnalyzer :
    def __init__(self , client: MongoClient , config ):
        self.client=client 
        self.config=config
        self.logger=logging.getLogger(__name__)
        self.analysis_config=config.get('index_analysis')
        self.excluded_dbs=self.analysis_config.get('excluded_databases', ['admin', 'local', 'config'])
        self.min_unused_days=self.analysis_config.get('min_unused_days',7)
        self.slow_query_threshold=self.analysis_config.get('slow_query_threshold_ms', 100)

        self._cache={}
        self._cache_ttl=300
        self._last_analysis={}
    def analyze_all_indexes(self) :
        results={
            'unused_indexes':[] ,
            'duplicate_indexes': [],
            'large_indexes': []

        }
        try :
            unused=self._find_unused_indexes()
            results['unused_indexes'] = unused


            duplicates=self._find_duplicate_indexes()
            results['duplicate_indexes'] = duplicates


            large_indexes=self._find_large_indexes()
            results['large_indexes'] = large_indexes
        except Exception as e :
            self.logger.error(f"erreur : {e}")
        return results
    def _find_unused_indexes(self):
        unused_indexes=[]
        try :
            db_list=self.client.list_database_names()
            for db_name in db_list :
                if db_name in self.excluded_dbs :
                     continue
                db=self.client[db_name]
                for collection_name in db.list_collection_names() :
                    try : 
                        collection= db[collection_name]
                        index_stats=list(collection.aggregate([{"$indexStats": {}}]))
                        for index_stat in index_stats :
                            index_name= index_stat['name']
                            if index_name=='_id_' :
                                continue
                            usage_count=index_stat['accesses']['ops']
                            since_date=index_stat['accesses'].get('since')

                            is_unused=False 

                            if usage_count==0 :
                                is_unused=True 
                            elif since_date and self.min_unused_days>0 :
                                days_since=(datetime.now() - since_date).days
                                if days_since> self.min_unused_days :
                                    is_unused=True 
                            if is_unused:
                                index_info=self._get_index_details(db, collection_name, index_name)
                            unused_indexes.append({
                                    'database': db_name,
                                    'collection': collection_name,
                                    'index_name': index_name,
                                    'key': index_stat.get('key', {}),
                                    'usage_count': usage_count,
                                    'since': since_date,
                                    'size_bytes': index_info.get('size', 0),
                                    'unique': index_info.get('unique', False),
                                    'sparse': index_info.get('sparse', False),
                                    'compound': len(index_stat.get('key', {})) > 1
                                })
                    except Exception as e :
                        self.logger.error(f"erreur indexe : {e}")
        except Exception as e :
            self.logger.error(f"erreur dans la recherche des indexe {e}")
        return unused_indexes
    

    def _get_index_details(self, db , collection_name , index_name) :
        collection =db[collection_name]
        indexes = list(collection.list_indexes())
        for index in indexes :
            if index['name'] == index_name :
                return index 
    def _find_duplicate_indexes(self) :
        duplicate_indexes=[]

        try :
            db_liste=self.client.list_database_names()
            for db_name in db_liste :
                if db_name in self.excluded_dbs :
                    continue 
                db=self.client[db_name]
                for collection_name in db.list_collection_names():
                    try :
                        collection=db[collection_name]
                        indexes=collection.list_indexes()
                        indexes_grp= {}

                        for index in indexes :
                            key =tuple(sorted(index['key'].items()))
                            if key not in indexes_grp:
                                indexes_grp[key]=[]
                            indexes_grp[key].append(index)
                        for key , list_index in indexes_grp.items():
                            if len(list_index)>1 :
                                duplicate_indexes.append({
                                    'database' : db_name ,
                                    'collection' : collection_name ,
                                    'key' : dict(key) ,
                                    'count': len(list_index),
                                    'type':'exact_duplicate' })
                    except Exception as e :
                        self.logger.error(f"erreur detection {e}")
        except Exception as e :
            self.logger.error(f"erreur detection index duplique {e}")
        return duplicate_indexes
    def _find_large_indexes(self) :
        large_indexes=[]
        size_threshold=self.analysis_config.get('large_index_threhold_mb' , 100)
        try :
            db_liste=self.client.list_database_names() 
            for db_name in db_liste :
                if db_name in self.excluded_dbs :
                    continue
                db=self.client[db_name]
                for collection_name in db._list_collection_names() :
                    try : 
                        collection= db[collection_name]
                         
                        stats = db.command('collStats', collection_name, indexDetails=True)
                        if 'indexSizes' in stats :
                            for index_name , size_bytes in stats['indexSizes'].items():
                                size_mb=size_bytes/(1024*1024)
                                if size_mb>size_threshold :
                                    large_indexes.append({
                                        'database': db_name,
                                        'collection': collection_name,
                                        'index_name': index_name,
                                        'size_bytes': size_bytes,
                                    })

                    except Exception as e :
                        self.logger.error(f"erreur {e}")
        except Exception as e :
            self.logger.error(f"Erreur recherche gros index : {e}")
        return large_indexes
                    

         

       


                        




                                    




            





