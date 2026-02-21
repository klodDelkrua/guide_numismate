########################################################################
#Project : guide numismate                                              #
# Python + PostgreSQL                                                   #
#created by Claude Delcroix                                             #
# Date : 13.12.2025                                                     #
#########################################################################
from ui import  run_application
from repository import NumismateRepository, SessionLocal, engine
from sqlalchemy import text
def main():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Connexion à PostgreSQL établie avec succès !")
    except Exception as e:
        print(f"❌ Échec critique de connexion : {e}")
        return  # On arrête tout si la DB n'est pas là
    repo = NumismateRepository(SessionLocal)
    run_application(repo)

if __name__ == '__main__':

    main()
