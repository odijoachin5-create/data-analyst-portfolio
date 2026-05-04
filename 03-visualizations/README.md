# 📊 COVID-19 Global Visualization Dashboard

## 📋 Description
Analyse et visualisation complète de la pandémie COVID-19 à l'échelle mondiale.
Ce projet démontre la maîtrise de **Matplotlib** et **Seaborn** pour transformer
des données brutes en insights visuels communicables aux décideurs.

---

## 🎯 Objectifs
- Maîtriser les types de graphiques essentiels (line, bar, scatter, heatmap, violin, pie)
- Appliquer le storytelling visuel sur des données réelles
- Produire un dashboard multi-panels publication-ready
- Analyser une crise mondiale à travers les données

---

## 🛠️ Stack Technique
| Outil | Usage |
|-------|-------|
| Python 3.13 | Langage principal |
| Pandas | Nettoyage et manipulation |
| Matplotlib | Graphiques customisés, GridSpec layout |
| Seaborn | Graphiques statistiques (heatmap, violin, scatter) |
| Jupyter Notebook | Analyse interactive |

---

## 📊 Visualisations Produites

| # | Graphique | Type | Insight |
|---|-----------|------|---------|
| 1 | Evolution mondiale | Line + Bar | Progression des vagues |
| 2 | Top 10 pays | Barh | USA et Brésil en tête |
| 3 | Corrélations | Heatmap Seaborn | Mortalité vs guérisons |
| 4 | Distribution régions OMS | Boxplot + Violin | Disparités régionales |
| 5 | Cas vs Décès | Scatter annoté | Relation non linéaire |
| 6 | Dashboard final | Multi-panels | Vue 360 de la crise |

---

## 📈 Résultats Clés

### 🌍 Situation Mondiale
| KPI | Valeur |
|-----|--------|
| Cas confirmés totaux | 13.8M+ |
| Décès totaux | 588K+ |
| Taux de mortalité global | 4.26% |
| Pays touchés | 187 |

### Insights majeurs
1. **Les Amériques** concentrent la majorité des cas (40%+)
2. **Corrélation forte** entre cas confirmés et décès (r=0.98)
3. **Disparités régionales** : taux de mortalité très variable selon la région OMS
4. **Effet de vague** clairement visible sur les nouveaux cas journaliers
5. **Moyenne mobile 7 jours** révèle les tendances derrière le bruit quotidien

---

## 📁 Structure du Projet
    03-visualizations/
    ├── jour3_visualizations_covid.ipynb      # Notebook complet
    ├── covid_evolution_mondiale.png          # Graphique 1
    ├── covid_top10_pays.png                  # Graphique 2
    ├── covid_heatmap_correlations.png        # Graphique 3
    ├── covid_distribution_regions.png        # Graphique 4
    ├── covid_scatter_confirmed_deaths.png    # Graphique 5
    ├── covid_dashboard_final.png             # Dashboard final
    └── README.md                             # Documentation

---

## 💡 Compétences Démontrées
- Customisation avancée Matplotlib (GridSpec, annotations, formatters)
- Graphiques statistiques Seaborn (heatmap, violin, boxplot, scatter)
- Storytelling data-driven avec narration visuelle
- Dashboard multi-panels avec layout GridSpec
- Gestion des données temporelles et rolling averages

---

## 🔗 Source des Données
- [Kaggle - Corona Virus Report](https://www.kaggle.com/datasets/imdevskp/corona-virus-report)
- Données : Janvier 2020 — Juillet 2020

---

