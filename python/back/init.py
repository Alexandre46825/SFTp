from database import engine, Base
import models  # charge tous les modèles

Base.metadata.create_all(bind=engine)
print(" Tables créées avec succès")