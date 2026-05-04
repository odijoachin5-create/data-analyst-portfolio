# 🗄️ SQL Analysis — Superstore Database

## 📋 Description
Analyse SQL complète du dataset Superstore sur PostgreSQL 18.
Ce projet démontre la maîtrise du SQL analytique pour extraire
des insights business directement depuis une base de données relationnelle.

---

## 🛠️ Stack Technique
| Outil | Usage |
|-------|-------|
| PostgreSQL 18 | Base de données relationnelle |
| SQL | Requêtes analytiques |
| SQLAlchemy | Connexion Python-PostgreSQL |
| Pandas | Exploitation des résultats SQL |
| Matplotlib/Seaborn | Visualisation des insights |

---

## 🗃️ Base de Données
- **Base** : superstore_db
- **Table** : orders (9 994 lignes × 21 colonnes)
- **Période** : 2014 — 2017

---

## 📊 Requêtes Réalisées (20 requêtes)

| # | Requête | Concepts SQL |
|---|---------|-------------|
| 1 | Top 10 commandes | SELECT, LIMIT |
| 2 | Commandes en perte | WHERE, ORDER BY |
| 3 | Filtres discounts | WHERE >= |
| 4 | Filtres combinés | AND, multi-conditions |
| 5 | KPIs globaux | COUNT DISTINCT, SUM, AVG |
| 6 | Performance catégorie | GROUP BY, ROUND, NULLIF |
| 7 | Performance région | GROUP BY multi-colonnes |
| 8 | Sous-catégories en perte | HAVING, SUM négatif |
| 9 | Revenue mensuel | EXTRACT, GROUP BY date |
| 10 | Top clients | GROUP BY, ORDER BY DESC |
| 11 | Produits non rentables | HAVING SUM < 0 |
| 12 | Impact discount | CASE WHEN, tranches |
| 13 | Clients mixtes | CASE WHEN, HAVING complexe |
| 14 | Délai livraison | Arithmétique sur dates |
| 15 | Analyse annuelle | EXTRACT(YEAR) |
| 16 | Top villes | GROUP BY 3 colonnes |
| 17 | Segments clientèle | Marge calculée |
| 18 | Clients > moyenne | Sous-requête imbriquée |
| 19 | Top produits/catégorie | ROW_NUMBER() OVER |
| 20 | Région × Catégorie | Pivot SQL |

---

## 📈 Résultats Clés

### KPIs Globaux
| Métrique | Valeur |
|----------|--------|
| Revenue total | 2 297 201 USD |
| Profit total | 286 397 USD |
| Marge globale | 12.47% |
| Clients uniques | 793 |
| Commandes | 5 009 |

### Insights SQL Majeurs

#### Performance par Catégorie
| Catégorie | Revenue | Profit | Marge |
|-----------|---------|--------|-------|
| Technology | 836 154 USD | 145 455 USD | 15.61% |
| Office Supplies | 719 047 USD | 122 491 USD | 13.80% |
| Furniture | 741 999 USD | 18 451 USD | 3.88% |

#### Sous-catégories en perte
| Sous-catégorie | Perte |
|----------------|-------|
| Tables | -17 725 USD |
| Bookcases | -3 473 USD |
| Supplies | -1 189 USD |

#### Impact des discounts
- Discount 0% → profit moyen positif
- Discount > 30% → pertes systématiques
- Seuil critique identifié à 20%

---

## 📉 Visualisations
![SQL Analysis](sql_analysis.png)

---

## 💡 Recommandations
1. **Arrêter les discounts > 20%** : destruction systématique de valeur
2. **Audit Furniture** : Tables et Bookcases en perte chronique
3. **Focus West + Technology** : combinaison la plus rentable (23.82% de marge)
4. **Segment Corporate** : meilleur ratio commandes/profit

---

## 📁 Fichiers
- jour4_sql_analysis.ipynb : Notebook Python + SQL
- sql_analysis.png : Visualisations des résultats

---

*Projet réalisé dans le cadre d un parcours intensif Data Analyst — Jour 4/28*
