 

import logging
from pymongo import MongoClient
from metrics_collector import MetricsCollector
from IndexAnalyzer import IndexAnalyzer

def test_simple():
    
    client = MongoClient('mongodb://localhost:27017')
    
    try:
      
        client.admin.command('ping')
        print("Connexion OK")
        print("Métriques collectées  ")
        collector= MetricsCollector("C:/Users/Admin/Desktop/mongodb_monitoring/config.yaml")
        metrics=collector.collect_all()
        print("Métriques collectées :")
        print(metrics)
        analyzer = IndexAnalyzer(client, "C:/Users/Admin/Desktop/mongodb_monitoring/config.yaml" )
        
        
        print(" Analyse en cours")
        results = analyzer.analyze_all_indexes()
         
        print(f" RÉSULTATS:")
        print(f"Index non utilisés: {len(results['unused_indexes'])}")
        print(f"Index dupliqués: {len(results['duplicate_indexes'])}")
        print(f"Gros index: {len(results['large_indexes'])}")
         
        if results['unused_indexes']:
            print(f"\n Index non utilisés:")
            for idx in results['unused_indexes']:  
                print(f"   {idx['database']}.{idx['collection']}.{idx['index_name']}")
        
        if results['duplicate_indexes']:
            print(f"\ Index dupliqués:")
            for idx in results['duplicate_indexes']:
                print(f"   {idx['database']}.{idx['collection']}: {idx['duplicate_indexes']}")
        
        if results['large_indexes']:
            print(f"\n Gros index:")
            for idx in results['large_indexes'][:5]:
                print(f"   {idx['database']}.{idx['collection']}.{idx['index_name']}: {idx.get('size_mb', 'N/A')} MB")
        
       
        
    except Exception as e:
        print(f" Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    
    
    test_simple()