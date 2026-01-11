from src.guide_numismate.numismate import NumismateRepository
from func import *

def menu_1() -> int:
    print("\n--- Справочник нумизмата (Guide du Numismate) ---")
    print("\n[ GESTION DE MA COLLECTION ]")
    print(" 1. Ajouter un nouvel exemplaire (Pièce personnelle)")
    print(" 2. Modifier/Mettre à jour un exemplaire")
    print(" 3. Supprimer un exemplaire")

    print("\n[ CATALOGUE & RECHERCHE ]")
    print(" 4. Rechercher une Monnaie par Critère (Pays, Année, Valeur)")
    print(" 5. Voir toutes les Monnaies référencées")

    print("\n[ ANALYSE & VALORISATION ]")
    print(" 6. Synthèse de ma collection (Nombre de pièces, Valeur estimée)")
    print(" 7. Statistiques sur l'État de conservation")

    print("\n[ ADMINISTRATION (Avancé) ]")
    print(" 8. Gérer les Références (Ajouter/Modifier Pays, Monnaie, Variété)")

    print(" 0. Quitter")

    choice = int(input())
    while choice < 1 or choice > 8:
        choice = int(input())
    return choice

def run_application(repository: NumismateRepository):
    running = True
    while running:
        choice = menu_1()
        match choice:
            case 1:
                print("Lancement de l'ajout d'un exemplaire...")
                add_copy_workflow(repository)
        pass