from repository import NumismateRepository
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
        # Les autres champs String/Text sont pris tels quels, ou None si vide
        "purchase_currency": input("Devise d'achat (ex: EUR) : ") or None,
        "seller_source": input("Source/Vendeur : ") or None,
        "personal_comment": input("Commentaires personnels : ") or None,
    }

    succes = repository.add_copy(selected_variety_id, data)

    if succes:
        print("\n🎉 ~~~ SUCCESS : Nouvel exemplaire ajouté à la collection ! ~~~")
    else:
        print("\n❌ L'ajout de l'exemplaire a échoué. Vérifiez les données ou la connexion.")

def update_copy_workflow(repository: NumismateRepository):
    """Workflow pour modifier un exemplaire existant."""
    # 1. Selection de l'exemplaire a modifier
    collection = repository.get_user_collection()
    if not collection:
        print("\nVotre collection est vide. Rien a modifier.")
        return

    print("\n--- MES EXEMPLAIRES ---")
    for _, description in collection:
        print(description)

    try:
        copy_id = int(input("\nEntrez l'ID de l'exemplaire a modifier : "))
        if not any(item[0] == copy_id for item in collection):
            print("ID invalide.")
            return
    except ValueError:
        print("Entree invalide.")
        return

    print("\n--- MODIFICATION (Laissez vide pour ne pas changer la valeur actuelle) ---")

    #2. Saisie des nouvelles donnees (optionnelles)
    new_condition = input("Nouvel etat de conservation : ").strip()
    new_location = input("Nouvel emplacement physique : ").strip()
    new_price = safe_float_input("Nouveau prix d'achat : ", allow_none=True)
    new_value = safe_float_input("Nouvelle valeur estimee : ", allow_none=True)

    #3. Construction du dictionnaire de mise a jour (seulement ce qui est rempli)
    data = {}
    if new_condition: data["grading_condition"] = new_condition
    if new_location: data["physical_location"] = new_location
    if new_price is not None: data["purchase_price"] = new_price
    if new_value is not None: data["estimated_value"] = new_value

    if not data:
        print ("Aucun changement effectue.")
        return
    if repository.update_copy(copy_id, data):
        print(f"\nL'exemlaire {copy_id} a ete mis a jour avec succes !")
    else:
        print("\nEchec de la mise a jour.")

def delete_copy_workflow(repository: NumismateRepository):
    """Workflow pour supprimer un exemplaire de la collection."""
    #1. recuperation et affichage de la collection
    collection = repository.get_user_collection()
    if not collection:
        print("\nVotre collection est vide. Rien a supprimer.")
        return
    print("\n--- SUPPRESSION D'UN EXEMPLAIRE ---")
    for _, description in collection:
        print(description)

    #2. choice de l'ID
    try:
        copy_id = int(input("\nEntrez l'ID de l'exemplaire a supprimer (ou 0 pour annuler) : "))
        if copy_id == 0:
            return

        if not any(item[0] == copy_id for item in collection):
            print("Id non trouve dans votre collection.")
            return
    except ValueError:
        print("Entree invalide. Veuillez saisir un nombre.")
        return

    # 3. confirmation de securite
    confirm = input(f"Etes-vous sur de vouloir supprimer l'ID {copy_id} ? (oui/non) : ").lower()
    if confirm == "oui":
        if repository.delete_copy(copy_id):
            print(f"\n:L'exemplaire {copy_id} a ete retire de voitre collection.")
        else:
            print("\nLa suppression a echoue.")
    else:
        print("\nAnnulation de la suppression")

def search_coin_workflow(repository: NumismateRepository):
    """Workflow pour rechercher une monnaie dans le catalogue de reference"""
    print("\n--- RECHERCHER DANS LE CATALOGUE ---")
    print("(Laissez vide et appuyez sur Entree pour ignorer un critere)")

    country_search = input("Nom de pays : ").strip() or None
    year_input = input("Annee de frappe : ").strip()
    year_search = int(year_input) if year_input.isdigit() else None

    value_search = input("Valeur faciale (ex : 2, 50, 1/4) : ").strip() or None

    results = repository.search_catalogue(
        country_name=country_search,
        year=year_search,
        face_value=value_search
    )

    if not results:
        print("\nAucun resultat ne correspond a vos criteres.")
    else:
        print(f"\n{len(results)} resultat(s) trouve(s) :")
        for _, description in results:
            print(description)
        print("-" * 50)

def display_full_catalogue_workflow(repository: NumismateRepository):
    """Workflow pour afficher l'integralite du catalogue de reference."""
    print("\n" + "=" * 60)
    print("--- CATALOGUE COMPLET DES REFEREENCES ---")
    print("=" * 60)

    varieties = repository.get_varieties_for_selection()

    if not varieties:
        print("\nLe catalogue est actuellement vide.")
    else:
        #on affiche chaque ligne formatee
        for _, description in varieties:
            print(description)

    print("\n" + "=" * 60)
    input("Appuyez sur Entree pour revenir au menu principal...")


def collection_summary_workflow(repository: NumismateRepository):
    """Workflow pour afficher la synthèse financière de la collection."""
    print("\n--- SYNTHÈSE DE MA COLLECTION ---")

    stats = repository.get_collection_summary()

    if stats["total_count"] == 0:
        print("Votre collection est actuellement vide. Commencez par ajouter des exemplaires !")
        return

    print(f"📊 Nombre total de pièces : {stats['total_count']}")
    print(f"💰 Investissement total    : {stats['total_investment']:.2f} €")
    print(f"📈 Valeur estimée totale  : {stats['total_estimated_value']:.2f} €")

    # Petit bonus : Calcul de la plus-value latente
    profit = stats['total_estimated_value'] - stats['total_investment']
    color = "🟢" if profit >= 0 else "🔴"
    print(f"{color} Plus-value latente     : {profit:.2f} €")
    print("-" * 35)

def grading_stats_workflow(repository: NumismateRepository):
    """Workflow pour afficher les statistiques sur l'etat de conservation."""
    print("\n--- STATISTIQUES PAR ETAT DE CONSERVATION ---")
    stats = repository.get_grading_stats()

    if not stats:
        print("Aucune donnee a analyser.")
        return

    #Calcul du total pour le pourcentage
    total_copies = sum(count for _, count in stats)

    print(F"Total des exemplaires analyses : {total_copies}\n")

    for grade, count in stats:
        percentage = (count / total_copies) * 100
        bar = "#" * int(percentage / 5)
        print(f"{grade:<10} : {count:>3} ex. ({percentage:>5.1f}%) {bar}")

    print("-" * 50)

def admin_reference_workflow(repository: NumismateRepository):
    """Sous-menu pour la gestion des references catalogue."""
    print("\n--- ADMINISTRATION DES REFERENCES ---")
    print("1. Ajouter un pays")
    print("2. Ajouter un Type de Monnaie (ex: 2 Euro)")
    print("3. Ajouter une variete (ex: 2024 Atelier A)")
    print("0. Retour")

    choice = input("\nVotre choix : ")

    if choice == "1":
        name = input("Nom de pays : ")
        iso = input("Code ISO (3 lettres) : ")
        if repository.add_country(name, iso):
            print("Pays ajoute!")

    elif choice == "2":
        #On luste les pays pour avoir l'ID
        countries = repository.get_countries()
        for c in countries:
            print(f"[{c.id}] {c.name}")

        c_id = int(input("ID du pays emetteur : "))
        data = {
            "face_value": input("Valeur faciale : "),
            "currency_unit": input("Unité (Euro, Franc, etc.) : "),
            "metal_title": input("Métal : "),
            "diameter_mm": safe_float_input("Diamètre (mm) : "),
            "weight_g": safe_float_input("Poids (g) : ")
        }
        if repository.add_coin(c_id, data):
            print("Type de monnaie cree !")

    elif choice == "3":
        #pour simplifier, on pourrait lister les Coins ici comme on l'a fait pour les pays
        coins = repository.get_coins()
        for c in coins:
            print(f"[{c.id}] {c.name}")
        coin_id = int(input("ID du type de monnaie (Coin ID) : "))
        data = {
            "mintage_year": int(input("Année de frappe : ")),
            "mint_mark": input("Atelier (facultatif) : ") or None,
            "total_mintage": int(input("Tirage total (facultatif) : ") or 0)
        }
        if repository.add_variety(coin_id, data):
            print("Variete ajoutee au catalogue !")