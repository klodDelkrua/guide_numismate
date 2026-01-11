from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql.schema import UniqueConstraint
from typing import List, Tuple
# --------------------------
# Configuration de la Base de Données
# --------------------------
# NOTE : Remplacez par vos identifiants réels si le test passe.
DATABASE_URL = "postgresql://postgres:claude15delcroix@localhost:5432/numismate_db"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


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

        Retourne une liste de tuples: (variety_id, description_complete)
        """
        session = self.SessionFactory()
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
