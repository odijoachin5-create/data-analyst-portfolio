# 🎯 Analyse RFM — Segmentation Clients Superstore

![RFM Dashboard](rfm_dashboard.png)

## 📋 Description
Segmentation clients complète par analyse **RFM (Recency, Frequency, Monetary)** sur 793 clients
du dataset Superstore, entièrement réalisée en **SQL avancé** (CTEs chaînées + Window Functions NTILE).

Ce projet démontre une approche Data Scientist rigoureuse : détection et correction d une anomalie
de scoring, interprétation critique des résultats, et recommandations business actionnables.

---

## 🛠️ Stack Technique
| Outil | Usage |
|-------|-------|
| PostgreSQL 18 | Calcul RFM 100% en SQL |
| CTEs (WITH) | Pipeline en 4 étapes lisibles |
| NTILE(5) OVER | Scoring par quintiles |
| LAG / LEAD | Croissance temporelle |
| ROW_NUMBER / RANK | Classements par partition |
| SQLAlchemy | Connexion Python → PostgreSQL |
| Pandas | Agrégations post-SQL |
| Matplotlib | Dashboard 6 panels |

---

## 🔬 Méthodologie RFM

### Définition des dimensions
| Dimension | Question business | Calcul SQL |
|-----------|------------------|------------|
| **Recency (R)** | Depuis combien de jours le client a-t-il acheté ? | MAX(order_date) - date_référence |
| **Frequency (F)** | Combien de commandes a-t-il passé ? | COUNT(DISTINCT order_id) |
| **Monetary (M)** | Combien a-t-il dépensé au total ? | SUM(sales) |

### Scoring NTILE(5) — Quintiles
Chaque dimension est divisée en 5 quintiles (score 1 à 5) :

| Score | Recency | Frequency | Monetary |
|-------|---------|-----------|----------|
| 5 | Achat < 30 jours | > 10 commandes | > 5 000 USD |
| 4 | Achat 30-90 jours | 7-10 commandes | 3 000-5 000 USD |
| 3 | Achat 90-150 jours | 5-7 commandes | 1 500-3 000 USD |
| 2 | Achat 150-250 jours | 3-5 commandes | 500-1 500 USD |
| 1 | Achat > 250 jours | < 3 commandes | < 500 USD |

### Anomalie détectée et corrigée 🔍
Lors de l analyse, une **inversion du score Recency** a été détectée :
la requête initiale attribuait le score 5 aux clients les plus anciens.

**Correction appliquée** :
```sql
-- AVANT (incorrect) : récent → score 1
NTILE(5) OVER (ORDER BY recency_days ASC)

-- APRÈS (correct) : récent → score 5
NTILE(5) OVER (ORDER BY recency_days DESC)
```
Cette correction démontre l importance de la validation systématique des résultats
avant toute interprétation — réflexe fondamental en Data Science.

---

## 📊 Résultats par Segment

| Segment | Clients | % | Recency moy | Frequency moy | Monetary moy | Revenue total |
|---------|---------|---|-------------|---------------|--------------|---------------|
| Potentiel Loyaute | 337 | 42.5% | 130 jours | 7.14 commandes | 3 447 USD | 1 161 600 USD |
| Clients Fideles | 263 | 33.2% | 186 jours | 4.80 commandes | 1 418 USD | 372 988 USD |
| Hibernants | 105 | 13.2% | 196 jours | 8.58 commandes | 5 541 USD | 581 828 USD |
| Champions | 71 | 9.0% | 33 jours | 3.73 commandes | 733 USD | 52 011 USD |
| Nouveaux Clients | 17 | 2.1% | 37 jours | 10.29 commandes | 7 575 USD | 128 775 USD |

**Revenue total analysé : 2 297 201 USD**

---

## 🧠 Analyse Scientifique des Résultats

### Distribution statistique
| Métrique | Valeur |
|----------|--------|
| Total clients | 793 |
| Score RFM moyen | 8.99 / 15 |
| Score RFM médian | 9.00 / 15 |
| Écart-type | 2.48 |
| Recency moyenne | 147 jours |
| Frequency moyenne | 6.32 commandes |
| Monetary moyenne | 2 897 USD |

**Observation** : La quasi-égalité entre moyenne (8.99) et médiane (9.00) indique
une **distribution symétrique** des scores RFM — pas de biais majeur dans le scoring.
L écart-type de 2.48 révèle une **dispersion modérée** : les clients sont relativement
homogènes, sans groupes extrêmes très marqués.

---

### Matrice de corrélations RFM
| | Recency | Frequency | Monetary | Score Total |
|---|---------|-----------|----------|-------------|
| **Recency** | 1.000 | -0.384 | -0.143 | -0.098 |
| **Frequency** | -0.384 | 1.000 | 0.418 | -0.661 |
| **Monetary** | -0.143 | 0.418 | 1.000 | -0.614 |

**Interprétations statistiques :**

1. **Recency ↔ Frequency (r = -0.384)** : Corrélation négative modérée.
Les clients qui achètent fréquemment ont tendance à avoir acheté plus récemment.
Signal d un comportement d achat régulier.

2. **Frequency ↔ Monetary (r = +0.418)** : Corrélation positive modérée.
Plus un client commande souvent, plus son panier cumulé est élevé.
Relation attendue et cohérente économiquement.

3. **Recency ↔ Monetary (r = -0.143)** : Corrélation très faible.
Le montant dépensé ne prédit pas la récence d achat — les gros dépensiers
ne sont pas nécessairement les plus récents. Insight contre-intuitif.

4. **Frequency → Score Total (r = -0.661)** : Corrélation forte et négative.
La fréquence est le **facteur le plus discriminant** du score RFM.
Cela indique que la fidélité comportementale (fréquence) prime sur la valeur monétaire.

---

### Insights critiques par segment

#### 🏆 Champions (71 clients, 9%) — Potentiel à développer
Recency très faible (33 jours ✅) mais monetary bas (733 USD).
Ce sont des clients **récemment acquis** dont la valeur n est pas encore
pleinement développée. Priorité : augmenter le panier moyen via cross-sell.

#### ⚠️ Hibernants (105 clients, 13.2%) — Alerte critique
**Insight majeur** : monetary moyen de 5 541 USD et frequency de 8.58
mais recency de 196 jours. Ce segment représente en réalité des
**clients à très haute valeur historique en train de décrocher**.
Revenue total : 581 828 USD à risque de perdre définitivement.
Action urgente requise.

#### 🌟 Nouveaux Clients (17 clients, 2.1%) — Anomalie positive
Monetary moyen de 7 574 USD (le plus élevé de tous les segments) avec
une recency de 37 jours. Ces 17 clients sont probablement des
**comptes Corporate ou des acheteurs en volume** récemment acquis.
Traitement VIP immédiat recommandé.

#### 📊 Potentiel Loyauté (337 clients, 42.5%) — Le cœur du business
Ce segment dominant représente 50.6% du revenue total (1 161 600 USD).
C est la **base client principale** à convertir en Clients Fidèles.

---

## 💡 Recommandations Business par Segment

### 🏆 Champions — Nurturing & Upsell
- Proposer des produits premium et nouvelles catégories
- Programme d onboarding approfondi pour augmenter le panier
- Objectif : faire passer monetary de 733 USD à 2 000 USD en 6 mois

### ⚠️ Hibernants — Réactivation d urgence (581 828 USD à risque)
- Campagne de réactivation immédiate avec offre personnalisée
- Appel commercial direct pour les 20 plus gros comptes
- Analyse des raisons de décrochage (prix, concurrence, satisfaction)
- Budget recommandé : 10-15% du revenue à risque en actions marketing

### 🌟 Nouveaux Clients — Traitement VIP
- Account manager dédié pour ces 17 comptes stratégiques
- Contrat cadre avec conditions préférentielles
- Objectif : fidéliser ces comptes à fort potentiel

### 📊 Potentiel Loyauté — Conversion prioritaire
- Programme de fidélité avec paliers de récompenses
- Campagnes ciblées sur les catégories non achetées (cross-sell)
- Email nurturing mensuel avec recommandations personnalisées

### 💙 Clients Fidèles — Rétention
- Reconnaissance et avantages exclusifs
- Sollicitation pour avis et recommandations (NPS)
- Invitation aux événements clients et nouveautés

---

## ⚠️ Limites & Perspectives

### Limites de l analyse
1. **Pas de données démographiques** : l analyse RFM est purement comportementale
2. **Période figée** : snapshot 2014-2017, les tendances récentes ne sont pas capturées
3. **Seuils arbitraires** : les seuils de segmentation (13, 10, 7) méritent une calibration
   par test A/B sur les campagnes marketing réelles
4. **Absence de CLV** : le Customer Lifetime Value prédictif nécessiterait
   un modèle de régression ou de survie sur données historiques plus longues

### Améliorations possibles
- Modèle prédictif de churn (Random Forest ou Gradient Boosting)
- Segmentation par K-Means pour des clusters non supervisés
- Calcul du CLV par segment avec modèle pareto/NBD

---

## 📁 Fichiers
- jour5_rfm_analysis.ipynb : Notebook SQL + Python complet
- rfm_dashboard.png : Dashboard 6 panels

---

## 🔗 Source des Données
- [Kaggle — Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

---

*Projet réalisé dans le cadre d un parcours intensif Data Analyst — Jour 5/28*
