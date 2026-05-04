# 🗄️ SQL Analytics — Superstore Database (PostgreSQL)

![SQL Analysis](sql_analysis.png)

## 📋 Description
Analyse SQL complète du dataset Superstore sur **PostgreSQL 18**, couvrant **9 994 transactions**
sur 4 ans (2014-2017). Ce projet démontre la maîtrise du SQL analytique — des fondamentaux
aux requêtes avancées — pour extraire des insights business directement depuis une base
de données relationnelle, sans passer par Python.

L intégration SQLAlchemy permet ensuite de visualiser les résultats avec Pandas et Matplotlib.

---

## 🛠️ Stack Technique
| Outil | Version | Usage |
|-------|---------|-------|
| PostgreSQL | 18.3 | Base de données relationnelle |
| SQL | — | Requêtes analytiques (20 requêtes) |
| psycopg2 | 2.x | Driver Python-PostgreSQL |
| SQLAlchemy | 2.x | ORM et connexion Python |
| Pandas | 2.x | Exploitation et transformation des résultats |
| Matplotlib/Seaborn | — | Visualisation des insights SQL |

---

## 🗃️ Modèle de Données
    Table : orders
    ├── Identifiants    : row_id, order_id, customer_id, product_id
    ├── Temporel        : order_date, ship_date
    ├── Géographie      : country, city, state, postal_code, region
    ├── Client          : customer_name, segment
    ├── Produit         : category, sub_category, product_name, ship_mode
    └── Financier       : sales, quantity, discount, profit

- **Volume** : 9 994 lignes × 21 colonnes
- **Période** : Janvier 2014 — Décembre 2017
- **Encodage** : LATIN1 (import avec spécification explicite)
- **Datestyle** : MDY (format américain MM/DD/YYYY)

---

## 📊 KPIs Globaux
| Métrique | Valeur |
|----------|--------|
| Chiffre d affaires total | 2 297 201 USD |
| Profit total | 286 397 USD |
| Marge globale | 12.47% |
| Commandes uniques | 5 009 |
| Clients uniques | 793 |
| Panier moyen | 229.86 USD |

---

## 📝 Requêtes SQL Réalisées (20 requêtes)

### Fondamentaux
| # | Requête | Concepts |
|---|---------|----------|
| 1 | Top 10 commandes | SELECT, LIMIT |
| 2 | Commandes en perte | WHERE, ORDER BY |
| 3 | Filtres discounts élevés | WHERE >= |
| 4 | Filtres multi-conditions | AND, OR |
| 5 | KPIs globaux | COUNT DISTINCT, SUM, AVG, ROUND |

### Agrégations & Groupements
| # | Requête | Concepts |
|---|---------|----------|
| 6 | Performance par catégorie | GROUP BY, NULLIF, marge calculée |
| 7 | Performance par région | GROUP BY, ORDER BY DESC |
| 8 | Sous-catégories en perte | HAVING, SUM négatif |
| 9 | Revenue mensuel | EXTRACT(YEAR/MONTH), GROUP BY date |
| 10 | Top 10 clients | Multi-agrégations, ranking |

### Analyses Avancées
| # | Requête | Concepts |
|---|---------|----------|
| 11 | Produits jamais rentables | HAVING SUM < 0, multi-colonnes |
| 12 | Impact discount par tranche | CASE WHEN, segmentation |
| 13 | Clients mixtes profit/perte | CASE WHEN dans HAVING |
| 14 | Délai livraison par mode | Arithmétique sur dates |
| 15 | Performance année par année | EXTRACT, tendance temporelle |
| 16 | Top 5 villes | GROUP BY 3 colonnes |
| 17 | Analyse par segment | Marge calculée, ratio |
| 18 | Clients au-dessus de la moyenne | Sous-requête imbriquée |
| 19 | Top 3 produits par catégorie | ROW_NUMBER() OVER PARTITION BY |
| 20 | Matrice Région × Catégorie | Pivot SQL, analyse croisée |

---

## 📈 Résultats & Insights

### 1. Performance par Catégorie
| Catégorie | Commandes | Revenue | Profit | Marge |
|-----------|-----------|---------|--------|-------|
| Technology | 1 544 | 836 154 USD | 145 455 USD | 15.61% |
| Office Supplies | 3 742 | 719 047 USD | 122 491 USD | 13.80% |
| Furniture | 1 764 | 741 999 USD | 18 451 USD | 3.88% |

**Insight** : Furniture génère plus de revenue qu Office Supplies mais 6x moins de profit.
Signe d une structure de coûts problématique, pas d un problème de volume.

---

### 2. Performance par Région
| Région | Clients | Revenue | Profit |
|--------|---------|---------|--------|
| West | 686 | 725 458 USD | 108 418 USD |
| East | 674 | 678 781 USD | 91 523 USD |
| South | 512 | 391 722 USD | 46 749 USD |
| Central | 629 | 501 240 USD | 39 706 USD |

**Insight** : Central a plus de clients que South mais moins de profit.
Problème de mix produit ou de politique de discount agressive dans cette région.

---

### 3. Sous-catégories en Perte Chronique
| Sous-catégorie | Perte totale |
|----------------|-------------|
| Tables | -17 725 USD |
| Bookcases | -3 473 USD |
| Supplies | -1 189 USD |

**Insight** : Ces 3 sous-catégories détruisent 22 387 USD de valeur sur 4 ans.
Requête HAVING utilisée pour les isoler automatiquement.

---

### 4. Impact des Discounts (CASE WHEN)
| Tranche | Commandes | Profit moyen |
|---------|-----------|-------------|
| 0% | 4 580 | +65.27 USD |
| 1-20% | 2 714 | +18.43 USD |
| 21-30% | 1 562 | -22.18 USD |
| 30%+ | 1 138 | -89.54 USD |

**Insight critique** : Le seuil de rentabilité est à 20% de discount.
Au-delà, chaque transaction est une perte nette — résultat obtenu via CASE WHEN.

---

### 5. Matrice Région × Catégorie (Requête 20)
| Région | Catégorie | Marge |
|--------|-----------|-------|
| West | Office Supplies | 23.82% ✅ |
| East | Office Supplies | 19.96% ✅ |
| Central | Furniture | -1.75% ❌ |
| East | Furniture | 1.46% ⚠️ |

**Insight** : Central/Furniture est la combinaison la plus destructrice de valeur.
Aucune région ne rend Furniture suffisamment rentable.

---

### 6. Window Function — Top 3 Produits par Catégorie
Requête utilisant ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(sales) DESC)
pour identifier les 3 meilleurs produits dans chaque catégorie sans sous-requête multiple.

**Concept clé** : PARTITION BY divise le dataset en fenêtres, ORDER BY classe à l intérieur
— équivalent d un GROUP BY qui garde toutes les lignes.

---

## 📉 Visualisations
![SQL Analysis Dashboard](sql_analysis.png)
*3 panels : Revenue par catégorie | Marge % par catégorie | Profit moyen par tranche de discount*

---

## 🔌 Intégration Python — SQLAlchemy
```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:password@localhost/superstore_db')
df = pd.read_sql(query, engine)
```
Les résultats SQL sont chargés directement en DataFrame Pandas pour visualisation.
Zéro export CSV intermédiaire — pipeline direct DB → DataFrame → Visualisation.

---

## 💡 Recommandations Business

1. **Politique discount** : Plafonner strictement à 20% — au-delà c est une subvention déguisée
2. **Restructuration Furniture** : Tables et Bookcases en perte sur 4 ans → révision tarifaire ou retrait
3. **Benchmark West** : La région West avec Office Supplies atteint 23.82% de marge → dupliquer ce modèle
4. **Focus Corporate** : Le segment Corporate génère le meilleur ratio profit/commande
5. **Alerte Central** : Région la plus peuplée en clients mais la moins profitable → audit commercial urgent

---

## ⚙️ Setup & Reproduction
```bash
# 1. Démarrer PostgreSQL
sudo service postgresql start

# 2. Créer la base
sudo -u postgres psql -c "CREATE DATABASE superstore_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE superstore_db TO dataanalyst;"

# 3. Importer les données
sudo -u postgres psql -d superstore_db -c "\COPY orders FROM 'superstore.csv' DELIMITER ',' CSV HEADER ENCODING 'LATIN1';"

# 4. Lancer le notebook
jupyter notebook jour4_sql_analysis.ipynb
```

---

## 🔗 Source des Données
- [Kaggle — Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- Période : Janvier 2014 — Décembre 2017

---

*Projet réalisé dans le cadre d un parcours intensif Data Analyst — Jour 4/28*
