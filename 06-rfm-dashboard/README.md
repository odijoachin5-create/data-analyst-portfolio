# 🎯 RFM Interactive Dashboard — Dash & Plotly

## 📋 Description
Dashboard analytique interactif construit avec **Dash & Plotly** connecté en temps réel
à **PostgreSQL**. Ce projet représente l aboutissement des Jours 4-5-6 :
pipeline complet **SQL → Machine Learning → Dashboard interactif déployé**.

Le dashboard permet à n importe quel décideur non-technique d explorer
la segmentation RFM, le risque de churn et les clusters clients sans
écrire une seule ligne de code.

---

## 🛠️ Stack Technique
| Outil | Usage |
|-------|-------|
| Python 3.13 | Langage principal |
| Dash 2.x | Framework dashboard web |
| Plotly | Graphiques interactifs |
| Dash Bootstrap | UI dark theme professionnel |
| PostgreSQL 18 | Source de données live |
| SQLAlchemy | Connexion Python → DB |
| Scikit-learn | KMeans + Random Forest |
| Pandas / NumPy | Transformation des données |

---

## 🚀 Architecture du Projet

    PostgreSQL DB
         ↓
    SQLAlchemy (query SQL avec CTEs + Window Functions)
         ↓
    Pandas DataFrame (793 clients)
         ↓
    ┌────────────────────────────────┐
    │  Feature Engineering          │
    │  - Recency / Frequency /      │
    │    Monetary                   │
    │  - NTILE(5) scoring           │
    │  - Segmentation RFM           │
    │  - KMeans clustering          │
    │  - Churn prediction (RF)      │
    └────────────────────────────────┘
         ↓
    Dash App (4 tabs, 4 filtres, 9 graphiques)
         ↓
    localhost:8050

---

## 📊 KPIs Globaux
| Métrique | Valeur |
|----------|--------|
| Revenue total | 2 297 201 USD |
| Clients analysés | 793 |
| Taux de churn | 25.1% |
| Panier moyen | 2 897 USD |
| Revenue à risque | ~576 000 USD |
| Segments RFM | 5 |

---

## 🖥️ Fonctionnalités du Dashboard

### Filtres Globaux (temps réel)
- Segment RFM (Champions, A Risque, etc.)
- Région (West, East, Central, South)
- Statut Churn (Actif / Churné)
- Seuil probabilité de churn (slider 0-100%)

### Tab 1 — Vue Executive
| Graphique | Type | Insight |
|-----------|------|---------|
| Distribution segments | Donut chart | Répartition des 793 clients |
| Revenue par segment | Bar chart horizontal | Potentiel financier par groupe |
| Vue stratégique | Bubble chart | Position et poids de chaque segment |

### Tab 2 — Analyse RFM
| Graphique | Type | Insight |
|-----------|------|---------|
| Espace RFM | Scatter 3D interactif | Visualisation tri-dimensionnelle |
| Score R × F | Heatmap | Monetary moyen par combinaison de scores |
| Distribution monetary | Boxplot | Variance et outliers par segment |

### Tab 3 — Churn & ML
| Graphique | Type | Insight |
|-----------|------|---------|
| Distribution churn | Histogram overlay | Séparation Actifs vs Churnés |
| Feature importance | Bar chart | r_score = 70.87% du pouvoir prédictif |
| Clusters vs segments | Scatter | Validation croisée RFM ↔ KMeans |

### Tab 4 — Table Clients
- 793 lignes filtrables et triables
- Coloration conditionnelle par segment
- Export possible via interface
- Colonnes : Client, Segment, Région, Recency, Frequency, Monetary, Score RFM, Churn %

---

## 🔬 Pipeline ML Embarqué

### KMeans Clustering
- StandardScaler sur Recency, Frequency, Monetary
- K=3 optimal (Silhouette = 0.358)
- Labels automatiques : VIP, Réguliers, Inactifs

### Random Forest Churn
- Features : r_score, f_score, m_score, frequency, monetary
- Accuracy : 93% | F1-score churn : 0.85
- r_score = facteur #1 (70.87% importance)
- Seuil churn : recency > 180 jours

---

## 💡 Insights Clés Visibles dans le Dashboard

1. **Hibernants** : 13% des clients mais monetary moyen de 5 541 USD
   → Les clients les plus précieux sont en train de décrocher

2. **Champions** : recency 33 jours mais monetary faible
   → Clients récents à potentiel non encore développé

3. **r_score = 70.87% du churn**
   → La recency est le signal d alarme #1 à monitorer

4. **Potentiel Loyauté** : 42.5% des clients, 50.6% du revenue
   → Le cœur du business à fidéliser en priorité

---

## ⚙️ Installation & Lancement

```bash
# Installer les dépendances
pip install dash dash-bootstrap-components plotly sqlalchemy psycopg2-binary

# Démarrer PostgreSQL
sudo service postgresql start

# Lancer le dashboard
python app.py

# Ouvrir dans le navigateur
# http://localhost:8050
```

---

## 📁 Structure
    06-rfm-dashboard/
    ├── app.py        # Application Dash complète
    └── README.md     # Documentation

---

## 🔗 Projets liés
- Jour 4 : SQL Analysis (20 requêtes PostgreSQL)
- Jour 5 : RFM + KMeans + Churn Prediction
- Jour 6 : Ce dashboard (visualisation interactive)

---

*Projet réalisé dans le cadre d un parcours intensif Data Analyst — Jour 6/28*
