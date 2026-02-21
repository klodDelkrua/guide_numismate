from logic import *

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

    choice = int(input("Choix : "))
    while choice < 0 or choice > 8:
        choice = int(input("Erreur de choix\nChoix : "))
    return choice

def run_application(repository: NumismateRepository):
    running = True
    while running:
        choice = menu_1()
        match choice:
            case 0:
                print("Fin de session, Bye Bye")
                running = False
            case 1:
                print("Lancement de l'ajout d'un exemplaire...")
                add_copy_workflow(repository)
            case 2:
                update_copy_workflow(repository)
            case 3:
                delete_copy_workflow(repository)
            case 4:
                search_coin_workflow(repository)
            case 5:
                display_full_catalogue_workflow(repository)
            case 6:
                collection_summary_workflow(repository)
            case 7:
                grading_stats_workflow(repository)
            case 8:
                admin_reference_workflow(repository)