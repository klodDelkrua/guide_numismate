from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, Text, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql.schema import UniqueConstraint
from typing import List, Tuple
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")
# --------------------------
# Configuration de la Base de Données
# --------------------------
# NOTE : Remplacez par vos identifiants réels si le test passe.
DATABASE_URL = os.getenv("DB_NAME")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file.")
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

# --------------------------
# 1. Modèle Country
# --------------------------
class Country(Base):
    """Représente la table 'country' (Pays Émetteur)"""
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code_iso = Column(String(3), nullable=False, unique=True)

    # Relation : Un pays peut émettre plusieurs types de monnaie (One-to-Many)
    coins = relationship("Coin", back_populates="country", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Country(name='{self.name}', code_iso='{self.code_iso}')>"


# --------------------------
# 2. Modèle Coin (Type Général de Monnaie)
# --------------------------
class Coin(Base):
    """Représente la table 'coin' (Type de Monnaie)"""
    __tablename__ = "coin"

    # Ajout d'une contrainte UNIQUE pour garantir qu'un type de pièce est unique par Pays/Valeur/Unité
    __table_args__ = (
        UniqueConstraint('country_id', 'face_value', 'currency_unit', name='uq_coin_type'),
    )

    id = Column(Integer, primary_key=True)

    # Clé étrangère et Association (Côté DB)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)

    # L'attribut qui représente l'objet Pays (Côté Objet)
    country = relationship("Country", back_populates="coins")

    # Relation : Un type de monnaie a plusieurs variétés (One-to-Many)
    varieties = relationship("Variety", back_populates="coin", cascade="all, delete-orphan")

    # Attributs corrigés avec contraintes NOT NULL
    face_value = Column(String(50), nullable=False)
    currency_unit = Column(String(50), nullable=False)
    metal_title = Column(String(100), nullable=False)

    # IMPORTANT : Utilisation de Numeric pour la précision financière et des mesures
    diameter_mm = Column(Numeric(5, 2), nullable=False)
    weight_g = Column(Numeric(5, 2), nullable=False)

    shape = Column(String(50))
    edge_description = Column(String(100))

    # Utilisation de Text pour les longs descriptifs
    obverse_desc = Column(Text)
    reverse_desc = Column(Text)
    general_notes = Column(Text)  # Renommé de general_note pour la cohérence

    def __repr__(self):
        return f"<Coin({self.face_value} {self.currency_unit} - Country ID: {self.country_id})>"


# --------------------------
# 3. Modèle Variety (Émission Spécifique / Tirage)
# --------------------------
class Variety(Base):
    """Représente la table 'variety' (Émission Spécifique / Tirage)"""
    __tablename__ = "variety"

    # Contrainte UNIQUE pour garantir l'unicité par Coin/Année/Atelier
    __table_args__ = (
        UniqueConstraint('coin_id', 'mintage_year', 'mint_mark', name='uq_variety_edition'),
    )

    id = Column(Integer, primary_key=True)

    # Clé étrangère et Association (Côté DB)
    coin_id = Column(Integer, ForeignKey("coin.id"), nullable=False)

    # L'attribut qui représente l'objet Coin (Côté Objet)
    coin = relationship("Coin", back_populates="varieties")

    # Relation : Une variété a plusieurs exemplaires (One-to-Many)
    copies = relationship("Copy", back_populates="variety", cascade="all, delete-orphan")

    # Attributs corrigés
    mintage_year = Column(Integer, nullable=False)
    mint_mark = Column(String(50))
    total_mintage = Column(Integer)  # BIGINT en SQL correspond à Integer ou BigInteger en SQLAlchemy
    specific_variety_note = Column(String(255))
    finish_type = Column(String(50))
    catalogue_reference = Column(String(50))

    def __repr__(self):
        return f"<Variety({self.coin.face_value if self.coin else 'N/A'} - {self.mintage_year} {self.mint_mark})>"


# --------------------------
# 4. Modèle Copy (Exemplaire Personnel)
# --------------------------
class Copy(Base):
    """Représente la table 'copy' (Exemplaire Personnel)"""
    __tablename__ = "copy"

    id = Column(Integer, primary_key=True)

    # Clé étrangère et Association (Côté DB)
    variety_id = Column(Integer, ForeignKey("variety.id"), nullable=False)

    # L'attribut qui représente l'objet Variety (Côté Objet)
    variety = relationship("Variety", back_populates="copies")

    # Attributs corrigés avec contraintes NOT NULL
    grading_condition = Column(String(50), nullable=False)
    physical_location = Column(String(100), nullable=False)

    purchase_date = Column(Date)

    # Utilisation de Numeric pour la monnaie
    purchase_price = Column(Numeric(10, 2))
    purchase_currency = Column(String(10))

    seller_source = Column(String(100))
    estimated_value = Column(Numeric(10, 2))
    personal_comment = Column(Text)

    def __repr__(self):
        return f"<Copy(ID={self.id}, Grade='{self.grading_condition}', Loc='{self.physical_location}')>"

#----------------------------------------
#class de la gestion de la base de donnees
#-----------------------------------------

class NumismateRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add_copy(self, variety_id, data: dict):
        session = self.session_factory()
        try:
            new_copy = Copy(variety_id=variety_id, **data)
            session.add(new_copy)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout de l'exemplaire : {e}")
            return False
        finally:
            session.close()

    def get_varieties_for_selection(self) -> List[Tuple[int, str]]:
        """
        Récupère et formate les informations de toutes les variétés (Country, Coin, Variety)
        pour permettre à l'utilisateur de faire une sélection.

        Retourne une liste de tuples : (variety_id, description_complete)
        """
        session = self.session_factory()
        try:
            # Requête complexe : Sélectionne Variety, joint Coin, joint Country
            # Nous trions par Pays, puis par Valeur/Unité, puis par Année pour un affichage logique.
            results = (
                session.query(Variety, Coin, Country)
                .join(Coin, Variety.coin_id == Coin.id)
                .join(Country, Coin.country_id == Country.id)
                .order_by(Country.name, Coin.face_value, Coin.currency_unit, Variety.mintage_year.desc())
                .all()
            )

            selection_list = []

            # Formatage des résultats pour l'affichage
            for variety, coin, country in results:
                # Construit une description complète et facilement identifiable
                description = (
                    f"[{variety.id}] "
                    f"{country.name} - "
                    f"{coin.face_value} {coin.currency_unit} ({coin.metal_title}) - "
                    f"Année: {variety.mintage_year}"
                )

                # Ajout de l'atelier de frappe si renseigné
                if variety.mint_mark:
                    description += f" / Atelier: {variety.mint_mark}"

                # Ajout d'une note de variété spécifique si présente
                if variety.specific_variety_note:
                    description += f" ({variety.specific_variety_note})"

                selection_list.append((variety.id, description))

            return selection_list

        except Exception as e:
            print(f"Erreur lors de la récupération des variétés : {e}")
            return []
        finally:
            session.close()

    def update_copy(self, copy_id: int, update_data: dict) -> bool:
        """Met a jour un exemplaire existant avec les nouvelles donnees fournies."""
        session = self.session_factory()
        try:
            copy_to_update = session.query(Copy).filter(Copy.id == copy_id).first()
            if not copy_to_update:
                print(f"Exemplaire avec l'ID {copy_id} introuvable")
                return False
            #ON met a jour les attributs dynamiquement
            for key, value in update_data.items():
                if hasattr(copy_to_update, key):
                    setattr(copy_to_update, key, value)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de la mise a jour : {e}")
            return False
        finally:
            session.close()

    def get_user_collection(self) -> List[Tuple[int, str]]:
        """Recupere la liste des exemplaires possedes par l'utilisateur"""
        session = self.session_factory()
        try:
            # Jointure pour afficher des infos claires (Pays - Valuer - Etat)
            results = (
                session.query(Copy, Variety, Coin, Country)
                .join(Variety, Copy.variety_id == Variety.id)
                .join(Coin, Variety.coin_id == Coin.id)
                .join(Country, Coin.country_id == Country.id)
                .all()
            )
            return [(c.id, f"ID[{c.id}] {co.name}: {cn.face_value} {cn.currency_unit} ({c.grading_condition})")
                    for c, v, cn, co in results]
        finally:
            session.close()

    def delete_copy(self, copy_id: int) -> bool:
        """Supprime definitivement un exemplaire de la collection."""
        session = self.session_factory()
        try:
            #recherche de l'exemplaire
            copy_to_delete = session.query(Copy).filter(Copy.id == copy_id).first()
            if not copy_to_delete:
                print(f"Erreur : L'exemplaire ID {copy_id} n'existe pas.")
                return False

            #Suppression
            session.delete(copy_to_delete)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return False
        finally:
            session.close()

    def search_catalogue(self, country_name: str = None, year: int = None, face_value: str = None) -> List[Tuple[int, str]]:
        """Recherche dans le catalogue selon plusieurs critere combines."""
        session = self.session_factory()
        try:
            # on part d'une requete de bas avec toutes les jointures
            query = (
                session.query(Variety, Coin, Country)
                .join(Coin, Variety.coin_id == Coin.id)
                .join(Country, Coin.country_id == Country.id)
            )

            #On ajoute les filtres seulement si l'utilisateur a saisi quelque chose
            if country_name:
                #ilike permet une recherche insensible a la casse (ex : 'france' trouve 'France')
                query = query.filter(Country.name.ilike(f"%{country_name}%"))

            if year:
                query = query.filter(Variety.mintage_year_year == year)

            if face_value:
                query = query.filter(Coin.face_value.ilike(f"%{face_value}%"))

            results = query.order_by(Country.name, Variety.mintage_year.desc()).all()

            #formatage pour l'affichage
            return [
                (v.id, f"{co.name} | {cn.face_value} {cn.currency_unit} | Année: {v.mintage_year}")
                for v, cn, co in results
            ]
        finally:
            session.close()

    def get_collection_summary(self):
        """Calcule les statistiques globales de la collection personnelle."""
        session = self.session_factory()
        try:
            # on recupere : le compte total, la somme des prix d'achat et la somme des estimations
            stats = session.query(
                func.count(Copy.id),
                func.sum(Copy.purchase_price),
                func.sum(Copy.estimated_value)
            ).first()

            return {
                "total_count": stats[0] or 0,
                "total_investment": stats[1] or 0,
                "total_estimated_value": stats[2] or 0
            }
        finally:
            session.close()

    def get_grading_stats(self):
        """Recupere la repartition des exemplaires par etat de conservation."""
        session = self.session_factory()
        try:
            #On selectionne la colonne a grouper et le compte
            results = (
                session.query(
                    Copy.grading_condition,
                    func.count(Copy.id),
                )
                .group_by(Copy.grading_condition)
                .order_by(func.count(Copy.id).desc())
                .all()
            )
            return results
        finally:
            session.close()

    def add_country(self, name: str, code_iso: str):
        session = self.session_factory()
        try:
            new_country = Country(name=name, code_iso=code_iso.upper())
            session.add(new_country)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erreur Pays : {e}")
            return False
        finally:
            session.close()

    def add_coin(self, country_id: int, data: dict):
        session = self.session_factory()
        try:
            new_coin = Coin(country_id=country_id, **data)
            session.add(new_coin)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erreur Monnaie : {e}")
            return False
        finally:
            session.close()

    def add_variety(self, coin_id: int, data: dict):
        session = self.session_factory()
        try:
            new_variety = Variety(coin_id=coin_id, **data)
            session.add(new_variety)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erreur Variete : {e}")
            return False
        finally:
            session.close()

    def get_countries(self):
        session = self.session_factory()
        return session.query(Coin).all()

    def get_coins(self):
        session = self.session_factory()
        return session.query(Coin).all()