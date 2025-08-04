 

import logging
from pymongo import MongoClient
  # Votre fichier
from IndexAnalyzer import IndexAnalyzer

def test_simple():
    
    
     
    
    # Connexion (ajustez si nécessaire)
    client = MongoClient('mongodb://localhost:27017')
    
    try:
        # Test de connexion
        client.admin.command('ping')
        print("✅ Connexion OK")
        
        # Créer l'analyseur
        analyzer = IndexAnalyzer(client, "C:/Users/Admin/Desktop/mongodb_monitoring/config.yaml" )
        
        # Lancer l'analyse
        print("🔍 Analyse en cours...")
        results = analyzer.analyze_all_indexes()
        
        # Afficher les résultats
        print(f"\n📊 RÉSULTATS:")
        print(f"Index non utilisés: {len(results['unused_indexes'])}")
        print(f"Index dupliqués: {len(results['duplicate_indexes'])}")
        print(f"Gros index: {len(results['large_indexes'])}")
        
        # Détails si il y a des résultats
        if results['unused_indexes']:
            print(f"\n🔸 Index non utilisés:")
            for idx in results['unused_indexes'][:5]:  # Afficher les 5 premiers
                print(f"   {idx['database']}.{idx['collection']}.{idx['index_name']}")
        
        if results['duplicate_indexes']:
            print(f"\n🔸 Index dupliqués:")
            for idx in results['duplicate_indexes'][:5]:
                print(f"   {idx['database']}.{idx['collection']}: {idx['duplicate_indexes']}")
        
        if results['large_indexes']:
            print(f"\n🔸 Gros index:")
            for idx in results['large_indexes'][:5]:
                print(f"   {idx['database']}.{idx['collection']}.{idx['index_name']}: {idx.get('size_mb', 'N/A')} MB")
        
        print("✅ Test terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()

if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 TEST SIMPLE INDEXANALYZER")
    test_simple()