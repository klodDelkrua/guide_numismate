CREATE TABLE country(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code_iso VARCHAR(3) NOT NULL UNIQUE
);


CREATE TABLE coin (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Liaison essentielle
    country_id INTEGER NOT NULL,
    
    -- Identification principale (obligatoire)
    face_value VARCHAR(50) NOT NULL,
    currency_unit VARCHAR(50) NOT NULL,
    
    -- Caractéristiques physiques (obligatoire pour le catalogue)
    metal_title VARCHAR(100) NOT NULL,
    diameter_mm NUMERIC(5, 2) NOT NULL, -- Utilisation d'une précision pour les mesures
    weight_g NUMERIC(5, 2) NOT NULL,
    shape VARCHAR(50),
    edge_description VARCHAR(100),
    
    -- Descriptions
    obverse_desc TEXT, 
    reverse_desc TEXT, 
    general_notes TEXT,
    
    -- Contraintes de Clés
    CONSTRAINT fk_coin_country FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE RESTRICT,
    -- Empêche de supprimer un pays si des pièces y sont liées.
    
    -- Index Unique : un type de pièce est défini par son Pays, sa Valeur et son Unité.
    CONSTRAINT uq_coin_type UNIQUE (country_id, face_value, currency_unit) 
);


CREATE TABLE variety (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Liaison essentielle
    coin_id INTEGER NOT NULL,
    
    -- Identification (obligatoire)
    mintage_year INTEGER NOT NULL,
    mint_mark VARCHAR(50),
    
    -- Rareté
    total_mintage BIGINT,
    
    -- Spécifications
    specific_variety_note VARCHAR(255), -- Augmentation de la taille
    finish_type VARCHAR(50),
    catalogue_reference VARCHAR(50),
    
    -- Contraintes de Clés
    CONSTRAINT fk_variety_coin FOREIGN KEY (coin_id) REFERENCES coin(id) ON DELETE RESTRICT, 
    -- Un exemplaire de variété ne peut pas être orphelin d'un type de pièce.

    -- Index Unique : Le tirage est défini de manière unique par le Type, l'Année et l'Atelier.
    CONSTRAINT uq_variety_edition UNIQUE (coin_id, mintage_year, mint_mark)
);


CREATE TABLE copy (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Liaison essentielle
    variety_id INTEGER NOT NULL,
    
    -- État et localisation (obligatoire)
    grading_condition VARCHAR(50) NOT NULL, -- L'état de conservation est la base de la valeur
    physical_location VARCHAR(100) NOT NULL, -- Où la pièce est rangée
    
    -- Acquisition
    purchase_date DATE,
    purchase_price NUMERIC(10, 2),
    purchase_currency VARCHAR(10),
    seller_source VARCHAR(100),
    
    estimated_value NUMERIC(10, 2),
    personal_comment TEXT, -- Correction orthographique: personal_comment
    
    -- Contraintes de Clés
    CONSTRAINT fk_copy_variety FOREIGN KEY (variety_id) REFERENCES variety(id) ON DELETE RESTRICT,
    -- L'exemplaire doit toujours être lié à un type de variété
    
    -- Contrainte de vérification : le prix d'achat doit être positif
    CONSTRAINT chk_purchase_price CHECK (purchase_price >= 0) 
);