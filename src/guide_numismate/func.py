from numismate import *
import datetime

def select_variety_from_catalogue(repository: NumismateRepository) -> int | None:
    """Affiche la liste des variétés et demande à l'utilisateur de faire un choix par ID."""

    varieties_list = repository.get_varieties_for_selection()

    if not varieties_list:
        print("Le catalogue de référence est vide. Veuillez ajouter des Monnaies/Variétés d'abord.")
        return None

    print("\n--- SÉLECTION DE LA MONNAIE DE RÉFÉRENCE ---")

    # Affichage de la liste formatée
    for variety_id, description in varieties_list:
        print(description)

    print("-" * 50)

    while True:
        try:
            choice_id = input("Entrez l'ID [au crochet] de la monnaie à ajouter (ou 'q' pour annuler) : ")
            if choice_id.lower() == 'q':
                return None

            choice_id = int(choice_id)

            # Vérification simple que l'ID est dans la liste
            if any(item[0] == choice_id for item in varieties_list):
                return choice_id
            else:
                print("ID invalide. Veuillez réessayer.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro.")


# --- Fonctions utilitaires pour la validation ---

def safe_float_input(prompt: str, allow_none=True) -> float | None:
    """Demande une entrée et assure qu'elle est un nombre flottant ou None."""
    while True:
        value = input(prompt).strip()
        if not value and allow_none:
            return None
        try:
            return float(value)
        except ValueError:
            print("❌ Erreur de saisie : Veuillez entrer un nombre valide.")


def safe_date_input(prompt: str) -> datetime.date | None:
    """Demande une date au format AAAA-MM-JJ et la convertit en objet date."""
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return None
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Erreur de format : Veuillez utiliser le format AAAA-MM-JJ (ex: 2025-12-14).")


# --- Workflow principal révisé ---

def add_copy_workflow(repository: NumismateRepository):
    """Workflow complet pour ajouter un exemplaire avec validation d'entrée."""

    # Étape 1 : Sélection de la référence (Variety_id)
    # Nécessite que select_variety_from_catalogue(repository) soit défini et fonctionnel
    selected_variety_id = select_variety_from_catalogue(repository)

    if selected_variety_id is None:
        print("Ajout annulé.")
        return

    print(f"\nMonnaie sélectionnée (ID: {selected_variety_id}).")
    print("--- SAISIE DES DÉTAILS DE VOTRE EXEMPLAIRE ---")

    # Étape 2 : Saisie des détails personnels avec validation

    # Champs obligatoires (NOT NULL dans la DB)
    grading_condition = input("État de conservation (ex: FDC, TTB) [OBLIGATOIRE] : ").strip()
    physical_location = input("Emplacement physique [OBLIGATOIRE] : ").strip()

    if not grading_condition or not physical_location:
        print("❌ L'état et l'emplacement sont obligatoires. Ajout annulé.")
        return

    # Saisie sécurisée pour les nombres et les dates
    purchase_price = safe_float_input("Prix d'achat (0 si inconnu) : ", allow_none=True)
    estimated_value = safe_float_input("Valeur estimée actuelle : ", allow_none=True)
    purchase_date = safe_date_input("Date d'achat (AAAA-MM-JJ, optionnel) : ")

    data = {
        "grading_condition": grading_condition,
        "physical_location": physical_location,
        "purchase_date": purchase_date,
        "purchase_price": purchase_price,
        "estimated_value": estimated_value,
        # Les autres champs String/Text sont pris tels quels, ou None si vides
        "purchase_currency": input("Devise d'achat (ex: EUR) : ") or None,
        "seller_source": input("Source/Vendeur : ") or None,
        "personal_comment": input("Commentaires personnels : ") or None,
    }

    succes = repository.add_copy(selected_variety_id, data)

    if succes:
        print("\n🎉 ~~~ SUCCESS : Nouvel exemplaire ajouté à la collection ! ~~~")
    else:
        print("\n❌ L'ajout de l'exemplaire a échoué. Vérifiez les données ou la connexion.")