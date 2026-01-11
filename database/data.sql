-- Insertion des 10 Pays
INSERT INTO country (name, code_iso) VALUES 
('France', 'FRA'),
('États-Unis d''Amérique', 'USA'),
('Allemagne', 'DEU'),
('Canada', 'CAN'),
('Japon', 'JPN'),
('Australie', 'AUS'),
('Royaume-Uni', 'GBR'),
('Italie', 'ITA'),
('Chine', 'CHN'),
('Mexique', 'MEX');

-- Insertion des 10 Types de Monnaie (Coin)
-- (Incluant les 3 types de l'exemple de départ + 7 nouveaux)

-- 1. France - 1 Centime Euro
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'FRA'), '1', 'CENT', 'Acier plaqué cuivre', 16.25, 2.30, 'Ronde', 'Lisse', 'Marianne par Fabienne Courtiade', 'Globe avec valeur', NULL);

-- 2. USA - 1 Dollar Sacagawea
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'USA'), '1', 'DOLLAR', 'Cupro-nickel/Manganèse-laiton', 26.50, 8.10, 'Ronde', 'Lisse', 'Tête de Sacagawea', 'Aigle en vol', 'Pièce de circulation, coloris or.');

-- 3. Allemagne - 1 Euro
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'DEU'), '1', 'EURO', 'Bimétallique (CuNi, Laiton)', 23.25, 7.50, 'Ronde', 'Cannelée fine et segmentée', 'Aigle fédéral', 'Globe avec valeur', NULL);

-- 4. Canada - 1 Cent
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'CAN'), '1', 'CENT', 'Cuivre (jusqu''à 1996)', 19.05, 2.50, 'Ronde', 'Lisse', 'Reine Elizabeth II', 'Feuille d''érable', 'Pièce démonétisée.');

-- 5. Japon - 1 Yen
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'JPN'), '1', 'YEN', 'Aluminium', 20.00, 1.00, 'Ronde', 'Cannelée', 'Jeunes pousses', 'Valeur', 'La plus légère des pièces japonaises.');

-- 6. Royaume-Uni - 1 Livre (Moderne)
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'GBR'), '1', 'POUND', 'Bi-métallique (Nickel-laiton/CuNi)', 23.40, 8.75, 'Dodécagonale', 'Cannelée', 'Reine Elizabeth II', 'Les quatre nations', 'Nouvelle forme depuis 2017.');

-- 7. Italie - 500 Lires (Ancienne)
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'ITA'), '500', 'LIRE', 'Bi-métallique (Acrostal/Bronzital)', 29.00, 6.80, 'Ronde', 'Inscrite', 'Tête de femme de la Renaissance', 'Palais de la République', 'Démonétisée depuis le passage à l''Euro.');

-- 8. Chine - 1 Yuan (Pièce)
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'CHN'), '1', 'YUAN', 'Acier plaqué Nickel', 25.00, 6.10, 'Ronde', 'Cannelée', 'Nom du pays et année', 'Fleur de l''orchidée', NULL);

-- 9. Mexique - 10 Pesos (Pièce Commémorative Argent)
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'MEX'), '10', 'PESOS', 'Argent 999‰', 40.00, 31.10, 'Ronde', 'Cannelée', 'Armoiries nationales', 'Calendrier aztèque', 'Pièce d''investissement ou commémorative.');

-- 10. Australie - 50 Cents
INSERT INTO coin (country_id, face_value, currency_unit, metal_title, diameter_mm, weight_g, shape, edge_description, obverse_desc, reverse_desc, general_notes)
VALUES ((SELECT id FROM country WHERE code_iso = 'AUS'), '50', 'CENTS', 'Cupro-nickel', 31.50, 15.55, 'Dodécagonale', 'Cannelée', 'Reine Elizabeth II', 'Armoiries de l''Australie', 'Grande pièce dodécagonale.');

-- Insertion des Variétés (Variety)
-- Nous réinsérons les 4 premières pour avoir des IDs propres (1, 2, 3, 4) pour les tests Copy.

-- A. Monnaies de base (celles de l'exemple initial)

-- 1. Variety France 1 Cent 2000
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'FRA' AND c.face_value = '1' AND c.currency_unit = 'CENT'),
    2000, 'F', 1500000000, 
    '1ère série, Atelier de Pessac', 'Standard', 'KM# 1301'
);

-- 2. Variety USA 1 Dollar 2000 P 
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'USA' AND c.face_value = '1' AND c.currency_unit = 'DOLLAR'),
    2000, 'P', 767140000, 
    'Atelier de Philadelphie', 'Standard', 'KM# 310'
);

-- 3. Variety USA 1 Dollar 2000 D 
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'USA' AND c.face_value = '1' AND c.currency_unit = 'DOLLAR'),
    2000, 'D', 518900000, 
    'Atelier de Denver', 'Standard', 'KM# 310a'
);

-- 4. Variety Allemagne 1 Euro 2002 J
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'DEU' AND c.face_value = '1' AND c.currency_unit = 'EURO'),
    2002, 'J', 450000000, 
    'Atelier de Hambourg', 'Standard', 'KM# 209'
);

-- B. Les 6 Variétés supplémentaires (Celles qui généraient des erreurs)

-- 5. Variety France 1 Cent - Année 2001 (Moins courant)
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'FRA' AND c.face_value = '1' AND c.currency_unit = 'CENT'),
    2001, 'F', 20000000, 
    NULL, 'Standard', 'KM# 1301a'
);

-- 6. Variety USA 1 Dollar 2000 P - Finish 'Proof' (Pour tester le type de finition)
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'USA' AND c.face_value = '1' AND c.currency_unit = 'DOLLAR'),
    2000, 'P', 400000, 
    'Finition miroir', 'Proof (Épreuve)', 'KM# 310P'
);

-- 7. Variety Canada 1 Cent 1978 
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'CAN' AND c.face_value = '1' AND c.currency_unit = 'CENT'),
    1978, NULL, NULL, 
    'Feuille d''érable large', 'Standard', 'KM# 102'
);

-- 8. Variety Japon 1 Yen 1999 
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'JPN' AND c.face_value = '1' AND c.currency_unit = 'YEN'),
    1999, NULL, 120000000, 
    NULL, 'Standard', 'KM# Y96'
);

-- 9. Variety Royaume-Uni 1 Pound 2017
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'GBR' AND c.face_value = '1' AND c.currency_unit = 'POUND'),
    2017, NULL, 500000000, 
    '1ère année de la forme Dodécagonale', 'Standard', 'KM# 1400'
);

-- 10. Variety Mexique 10 Pesos (Commémorative)
INSERT INTO variety (coin_id, mintage_year, mint_mark, total_mintage, specific_variety_note, finish_type, catalogue_reference)
VALUES ( 
    (SELECT c.id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'MEX' AND c.face_value = '10' AND c.currency_unit = 'PESOS'),
    2020, NULL, 50000, 
    'Émission commémorative du Centenaire de la Constitution', 'Fleur de Coin (Proof)', 'KM# 700'
);


-- Insertion des 5 Exemplaires de Test (Copy)

-- 1. Exemplaire 1 : Le Centime Français (Variety ID 1)
INSERT INTO copy (variety_id, grading_condition, physical_location, purchase_date, purchase_price, purchase_currency, seller_source, estimated_value, personal_comment)
VALUES (
    (SELECT id FROM variety WHERE mintage_year = 2000 AND coin_id = (SELECT id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'FRA' AND c.face_value = '1')), 
    'TTB', 'Boîte à monnaie verte', '2024-05-15', 
    0.01, 'EUR', 'Trouvé en circulation', 0.05, 'Belle patine.'
);

-- 2. Exemplaire 2 : Le Dollar Sacagawea (Variety ID 2)
INSERT INTO copy (variety_id, grading_condition, physical_location, purchase_date, purchase_price, purchase_currency, seller_source, estimated_value, personal_comment)
VALUES (
    (SELECT id FROM variety WHERE mintage_year = 2000 AND mint_mark = 'P' AND coin_id = (SELECT id FROM coin c JOIN country cy ON c.country_id = cy.id WHERE cy.code_iso = 'USA' AND c.face_value = '1')), 
    'FDC', 'Coffret A, case 12', '2025-10-01', 
    15.00, 'USD', 'eBay (Vendeur NumisMax)', 20.00, 'Acheté pour sa qualité Fleur de Coin.'
);

-- 3. Exemplaire 3 : 1 Yen Japon (Très usé)
INSERT INTO copy (variety_id, grading_condition, physical_location, purchase_date, purchase_price, purchase_currency, seller_source, estimated_value, personal_comment)
VALUES (
    (SELECT v.id FROM variety v JOIN coin c ON v.coin_id = c.id JOIN country cy ON c.country_id = cy.id 
     WHERE v.mintage_year = 1999 AND cy.code_iso = 'JPN' AND c.face_value = '1'), 
    'TB', 'Boîte à monnaie noire, N° 3', '2024-01-10', 
    0.05, 'EUR', 'Vrac étranger', 0.05, 'Très léger et très usé.'
);

-- 4. Exemplaire 4 : 1 Livre UK (Acheté cher)
INSERT INTO copy (variety_id, grading_condition, physical_location, purchase_date, purchase_price, purchase_currency, seller_source, estimated_value, personal_comment)
VALUES (
    (SELECT v.id FROM variety v JOIN coin c ON v.coin_id = c.id JOIN country cy ON c.country_id = cy.id 
     WHERE v.mintage_year = 2017 AND cy.code_iso = 'GBR' AND c.face_value = '1'), 
    'UNC', 'Capsule scellée', '2025-02-20', 
    5.50, 'GBP', 'Distributeur spécialisé', 5.00, NULL
);

-- 5. Exemplaire 5 : 10 Pesos Mexique (Preuve)
INSERT INTO copy (variety_id, grading_condition, physical_location, purchase_date, purchase_price, purchase_currency, seller_source, estimated_value, personal_comment)
VALUES (
    (SELECT v.id FROM variety v JOIN coin c ON v.coin_id = c.id JOIN country cy ON c.country_id = cy.id 
     WHERE v.specific_variety_note LIKE 'Émission commémorative%' AND cy.code_iso = 'MEX' AND c.face_value = '10'), 
    'PF-70', 'Dalle NGC', '2024-12-01', 
    80.00, 'USD', 'Vente aux enchères (Sotheby''s)', 100.00, 'Pièce de la plus haute qualité disponible.'
);