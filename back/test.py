from database import engine

try:
    conn = engine.connect()
    print(" Connexion MySQL OK")
    conn.close()
except Exception as e:
    print(f" Erreur : {e}")