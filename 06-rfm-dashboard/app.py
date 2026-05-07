# ============================================================
# RFM Interactive Dashboard — Superstore Analytics
# Jour 6 — Data Analyst Portfolio
# ============================================================

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import dash
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. CONNEXION & DONNÉES
# ============================================================
engine = create_engine('postgresql://dataanalyst:nihcoaj@localhost/superstore_db')

query = """
WITH last_date AS (
    SELECT MAX(order_date) AS max_date FROM orders
),
client_rfm AS (
    SELECT
        customer_id,
        customer_name,
        MAX(segment)                   AS segment,
        MAX(region)                    AS region,
        MAX(order_date)                AS derniere_commande,
        COUNT(DISTINCT order_id)       AS frequency,
        ROUND(SUM(sales)::numeric, 2)  AS monetary
    FROM orders
    GROUP BY customer_id, customer_name
),
rfm_scores AS (
    SELECT c.*,
        (l.max_date - c.derniere_commande)                                AS recency_days,
        NTILE(5) OVER (ORDER BY (l.max_date - c.derniere_commande) DESC)  AS r_score,
        NTILE(5) OVER (ORDER BY c.frequency DESC)                          AS f_score,
        NTILE(5) OVER (ORDER BY c.monetary DESC)                           AS m_score
    FROM client_rfm c, last_date l
)
SELECT *,
    (r_score + f_score + m_score) AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score <= 2 AND (f_score + m_score) >= 8      THEN 'A Risque'
        WHEN f_score >= 4 AND m_score >= 3                  THEN 'Clients Fideles'
        WHEN r_score >= 4 AND f_score <= 2                  THEN 'Nouveaux Clients'
        WHEN (r_score + f_score + m_score) >= 7             THEN 'Potentiel Loyaute'
        ELSE 'Hibernants'
    END AS rfm_segment
FROM rfm_scores
ORDER BY rfm_total DESC
"""

df = pd.read_sql(query, engine)

# Churn label
df['churn']       = (df['recency_days'] > 180).astype(int)
df['churn_label'] = df['churn'].map({0: 'Actif', 1: 'Churné'})

# KMeans
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(df[['recency_days', 'frequency', 'monetary']])
km       = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = km.fit_predict(X_scaled)

cluster_profiles = df.groupby('cluster').agg(
    recency_moy  = ('recency_days', 'mean'),
    monetary_moy = ('monetary', 'mean')
).reset_index()
cluster_map = {}
for _, row in cluster_profiles.iterrows():
    if row['recency_moy'] < 100:
        cluster_map[row['cluster']] = 'Réguliers'
    elif row['monetary_moy'] > 3000:
        cluster_map[row['cluster']] = 'VIP'
    else:
        cluster_map[row['cluster']] = 'Inactifs'
df['cluster'] = df['cluster'].map(cluster_map)

# Churn model
X  = df[['r_score', 'f_score', 'm_score', 'frequency', 'monetary']]
y  = df['churn']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
df['churn_proba'] = rf.predict_proba(X)[:, 1]

# KPIs globaux
total_revenue   = df['monetary'].sum()
total_clients   = len(df)
churn_rate      = df['churn'].mean() * 100
avg_monetary    = df['monetary'].mean()
revenue_at_risk = df[df['churn'] == 1]['monetary'].sum()

print(f"✅ Données chargées : {total_clients} clients")
print(f"   Revenue total    : ${total_revenue:,.0f}")
print(f"   Churn rate       : {churn_rate:.1f}%")

# ============================================================
# 2. STYLES
# ============================================================
COLORS = {
    'Champions':         '#2ecc71',
    'Clients Fideles':   '#3498db',
    'Potentiel Loyaute': '#f39c12',
    'Nouveaux Clients':  '#9b59b6',
    'A Risque':          '#e74c3c',
    'Hibernants':        '#e67e22'
}

BG_COLOR   = '#0f1117'
CARD_COLOR = '#1a1d27'
TEXT_COLOR = '#ffffff'

card_style = {
    'backgroundColor': CARD_COLOR,
    'border':          '1px solid #2d3147',
    'borderRadius':    '12px',
    'padding':         '20px',
    'marginBottom':    '20px',
    'color':           TEXT_COLOR
}

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=TEXT_COLOR,
    margin=dict(l=40, r=20, t=40, b=40)
)

# ============================================================
# 3. LAYOUT
# ============================================================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)
app.title = "RFM Analytics Dashboard"


def kpi_card(title, value, subtitle, color='#3498db', icon='📊'):
    return dbc.Card([
        dbc.CardBody([
            html.Div(icon, style={'fontSize': '28px', 'marginBottom': '8px'}),
            html.H3(value, style={'color': color, 'fontWeight': 'bold',
                                  'margin': '0'}),
            html.P(title, style={'color': '#aaa', 'margin': '4px 0',
                                 'fontSize': '13px'}),
            html.Small(subtitle, style={'color': '#666', 'fontSize': '11px'})
        ])
    ], style={**card_style, 'textAlign': 'center', 'padding': '15px'})


app.layout = dbc.Container([

    # HEADER
    dbc.Row([
        dbc.Col([
            html.H1("🎯 RFM Analytics Dashboard",
                    style={'color': TEXT_COLOR, 'fontWeight': 'bold',
                           'fontSize': '28px', 'marginBottom': '4px'}),
            html.P("Superstore Customer Intelligence — Data Analyst Portfolio",
                   style={'color': '#888', 'fontSize': '13px'})
        ], width=8),
        dbc.Col([
            html.Div([
                html.Span("🟢 PostgreSQL Connected",
                          style={'color': '#2ecc71', 'fontSize': '12px'}),
                html.Br(),
                html.Span(f"{total_clients} clients analysés",
                          style={'color': '#888', 'fontSize': '11px'})
            ], style={'textAlign': 'right', 'paddingTop': '10px'})
        ], width=4)
    ], style={'marginBottom': '20px', 'marginTop': '20px'}),

    # FILTRES
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Segment RFM",
                               style={'color': '#aaa', 'fontSize': '12px'}),
                    dcc.Dropdown(
                        id='filter-segment',
                        options=[{'label': 'Tous', 'value': 'Tous'}] +
                                [{'label': s, 'value': s}
                                 for s in sorted(df['rfm_segment'].unique())],
                        value='Tous',
                        style={'backgroundColor': '#2d3147', 'color': '#000'}
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Région",
                               style={'color': '#aaa', 'fontSize': '12px'}),
                    dcc.Dropdown(
                        id='filter-region',
                        options=[{'label': 'Toutes', 'value': 'Toutes'}] +
                                [{'label': r, 'value': r}
                                 for r in sorted(df['region'].unique())],
                        value='Toutes',
                        style={'backgroundColor': '#2d3147', 'color': '#000'}
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Statut Churn",
                               style={'color': '#aaa', 'fontSize': '12px'}),
                    dcc.Dropdown(
                        id='filter-churn',
                        options=[
                            {'label': 'Tous',       'value': 'Tous'},
                            {'label': '🔴 Churné',  'value': 'Churné'},
                            {'label': '🟢 Actif',   'value': 'Actif'}
                        ],
                        value='Tous',
                        style={'backgroundColor': '#2d3147', 'color': '#000'}
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Seuil Probabilité Churn",
                               style={'color': '#aaa', 'fontSize': '12px'}),
                    dcc.Slider(
                        id='filter-proba',
                        min=0, max=1, step=0.1, value=0,
                        marks={0: '0%', 0.5: '50%', 1: '100%'}
                    )
                ], width=3)
            ])
        ])
    ], style={**card_style, 'marginBottom': '25px'}),

    # KPI CARDS
    dbc.Row([
        dbc.Col(kpi_card(
            "Revenue Total",
            f"${total_revenue:,.0f}",
            "2014-2017",
            '#2ecc71', '💰'), width=2),
        dbc.Col(kpi_card(
            "Clients Analysés",
            f"{total_clients:,}",
            "Clients uniques",
            '#3498db', '👥'), width=2),
        dbc.Col(kpi_card(
            "Taux de Churn",
            f"{churn_rate:.1f}%",
            "Inactifs > 180 jours",
            '#e74c3c', '⚠️'), width=2),
        dbc.Col(kpi_card(
            "Panier Moyen",
            f"${avg_monetary:,.0f}",
            "Par client",
            '#f39c12', '🛒'), width=2),
        dbc.Col(kpi_card(
            "Revenue à Risque",
            f"${revenue_at_risk:,.0f}",
            "Clients churnés",
            '#e74c3c', '🚨'), width=2),
        dbc.Col(kpi_card(
            "Segments RFM",
            str(df['rfm_segment'].nunique()),
            "Champions → Hibernants",
            '#9b59b6', '🎯'), width=2),
    ], style={'marginBottom': '25px'}),

    # TABS
    dbc.Tabs([

        # TAB 1 — VUE EXECUTIVE
        dbc.Tab(label="📊 Vue Executive", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Distribution des Segments",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-pie')])
                    ], style=card_style)
                ], width=5),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Revenue par Segment",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-revenue')])
                    ], style=card_style)
                ], width=7)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Bubble Chart — Vue Stratégique (Taille = Revenue)",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-bubble')])
                    ], style=card_style)
                ], width=12)
            ])
        ]),

        # TAB 2 — ANALYSE RFM
        dbc.Tab(label="🎯 Analyse RFM", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Scatter 3D — Espace RFM",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-3d')])
                    ], style=card_style)
                ], width=7),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Heatmap Score R × F",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-heatmap')])
                    ], style=card_style)
                ], width=5)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Distribution Monetary par Segment",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-box')])
                    ], style=card_style)
                ], width=12)
            ])
        ]),

        # TAB 3 — CHURN & ML
        dbc.Tab(label="🔮 Churn & ML", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Distribution Probabilité de Churn",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-churn-dist')])
                    ], style=card_style)
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Feature Importance — Random Forest",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-importance')])
                    ], style=card_style)
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "KMeans Clusters vs Segments RFM",
                            style={'color': TEXT_COLOR,
                                   'backgroundColor': CARD_COLOR}),
                        dbc.CardBody([dcc.Graph(id='graph-kmeans')])
                    ], style=card_style)
                ], width=12)
            ])
        ]),

        # TAB 4 — TABLE CLIENTS
        dbc.Tab(label="👥 Clients", children=[
            dbc.Card([
                dbc.CardHeader(
                    "Liste des Clients — Filtrable & Triable",
                    style={'color': TEXT_COLOR, 'backgroundColor': CARD_COLOR}),
                dbc.CardBody([
                    html.Div(id='table-stats',
                             style={'color': '#aaa', 'marginBottom': '10px',
                                    'fontSize': '13px'}),
                    dash_table.DataTable(
                        id='table-clients',
                        columns=[
                            {'name': 'Client',     'id': 'customer_name'},
                            {'name': 'Segment',    'id': 'segment'},
                            {'name': 'Région',     'id': 'region'},
                            {'name': 'Recency',    'id': 'recency_days'},
                            {'name': 'Frequency',  'id': 'frequency'},
                            {'name': 'Monetary',   'id': 'monetary'},
                            {'name': 'RFM Score',  'id': 'rfm_total'},
                            {'name': 'Segment RFM','id': 'rfm_segment'},
                            {'name': 'Churn %',    'id': 'churn_pct'},
                            {'name': 'Cluster',    'id': 'cluster'}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'backgroundColor': CARD_COLOR,
                            'color':           TEXT_COLOR,
                            'border':          '1px solid #2d3147',
                            'fontSize':        '12px',
                            'padding':         '8px'
                        },
                        style_header={
                            'backgroundColor': '#2d3147',
                            'color':           TEXT_COLOR,
                            'fontWeight':      'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query':
                                        '{rfm_segment} = "A Risque"'
                                },
                                'backgroundColor': '#3d1a1a',
                                'color':           '#e74c3c'
                            },
                            {
                                'if': {
                                    'filter_query':
                                        '{rfm_segment} = "Champions"'
                                },
                                'backgroundColor': '#1a3d2b',
                                'color':           '#2ecc71'
                            },
                            {
                                'if': {
                                    'filter_query':
                                        '{rfm_segment} = "Hibernants"'
                                },
                                'backgroundColor': '#3d2a1a',
                                'color':           '#e67e22'
                            },
                        ],
                        page_size=20,
                        sort_action='native',
                        filter_action='native',
                    )
                ])
            ], style=card_style)
        ])

    ], style={'marginBottom': '20px'}),

], fluid=True,
   style={'backgroundColor': BG_COLOR,
          'minHeight':       '100vh',
          'padding':         '0 20px'})


# ============================================================
# 4. CALLBACKS
# ============================================================
def filter_data(segment, region, churn_filter, proba_min):
    dff = df.copy()
    if segment != 'Tous':
        dff = dff[dff['rfm_segment'] == segment]
    if region != 'Toutes':
        dff = dff[dff['region'] == region]
    if churn_filter != 'Tous':
        dff = dff[dff['churn_label'] == churn_filter]
    dff = dff[dff['churn_proba'] >= proba_min]
    return dff


@callback(
    Output('graph-pie',        'figure'),
    Output('graph-revenue',    'figure'),
    Output('graph-bubble',     'figure'),
    Output('graph-3d',         'figure'),
    Output('graph-heatmap',    'figure'),
    Output('graph-box',        'figure'),
    Output('graph-churn-dist', 'figure'),
    Output('graph-importance', 'figure'),
    Output('graph-kmeans',     'figure'),
    Output('table-clients',    'data'),
    Output('table-stats',      'children'),
    Input('filter-segment',    'value'),
    Input('filter-region',     'value'),
    Input('filter-churn',      'value'),
    Input('filter-proba',      'value')
)
def update_all(segment, region, churn_filter, proba_min):
    dff = filter_data(segment, region, churn_filter, proba_min)

    # PIE
    seg_counts = dff['rfm_segment'].value_counts().reset_index()
    seg_counts.columns = ['segment', 'count']
    fig_pie = px.pie(
        seg_counts, values='count', names='segment',
        color='segment', color_discrete_map=COLORS, hole=0.4
    )
    fig_pie.update_layout(**PLOT_LAYOUT)
    fig_pie.update_traces(textinfo='label+percent', textfont_size=11)

    # REVENUE BAR
    rev = dff.groupby('rfm_segment')['monetary'].sum().reset_index()
    rev.columns = ['segment', 'revenue']
    rev = rev.sort_values('revenue', ascending=True)
    fig_rev = px.bar(
        rev, x='revenue', y='segment', orientation='h',
        color='segment', color_discrete_map=COLORS, text='revenue'
    )
    fig_rev.update_traces(
        texttemplate='$%{text:,.0f}', textposition='outside'
    )
    fig_rev.update_layout(**PLOT_LAYOUT, showlegend=False)

    # BUBBLE
    bubble = dff.groupby('rfm_segment').agg(
        recency   = ('recency_days', 'mean'),
        frequency = ('frequency',    'mean'),
        revenue   = ('monetary',     'sum'),
        clients   = ('customer_id',  'count')
    ).reset_index()
    fig_bubble = px.scatter(
        bubble,
        x='recency', y='frequency',
        size='revenue', color='rfm_segment',
        color_discrete_map=COLORS,
        hover_name='rfm_segment',
        hover_data={'clients': True, 'revenue': ':,.0f'},
        size_max=70, text='rfm_segment'
    )
    fig_bubble.update_traces(textposition='top center')
    fig_bubble.update_layout(
        **PLOT_LAYOUT,
        xaxis_title='Recency moyenne (jours) ← Récent | Ancien →',
        yaxis_title='Frequency moyenne',
        showlegend=False
    )
    fig_bubble.update_xaxes(autorange='reversed')

    # 3D SCATTER
    fig_3d = px.scatter_3d(
        dff,
        x='recency_days', y='frequency', z='monetary',
        color='rfm_segment', color_discrete_map=COLORS,
        hover_name='customer_name', opacity=0.7
    )
    fig_3d.update_layout(**PLOT_LAYOUT, height=450)

    # HEATMAP
    hmap = dff.groupby(
        ['r_score', 'f_score']
    )['monetary'].mean().reset_index()
    hmap_pivot = hmap.pivot(
        index='f_score', columns='r_score', values='monetary'
    )
    fig_heatmap = go.Figure(go.Heatmap(
        z=hmap_pivot.values,
        x=[f'R={c}' for c in hmap_pivot.columns],
        y=[f'F={i}' for i in hmap_pivot.index],
        colorscale='RdYlGn',
        text=np.round(hmap_pivot.values, 0),
        texttemplate='$%{text:,.0f}',
        showscale=True
    ))
    fig_heatmap.update_layout(
        **PLOT_LAYOUT,
        title='Monetary moyen par R×F'
    )

    # BOXPLOT
    fig_box = px.box(
        dff, x='rfm_segment', y='monetary',
        color='rfm_segment', color_discrete_map=COLORS,
        points='outliers'
    )
    fig_box.update_layout(
        **PLOT_LAYOUT, showlegend=False,
        xaxis_title='Segment', yaxis_title='Monetary (USD)'
    )

    # CHURN DISTRIBUTION
    fig_churn = px.histogram(
        dff, x='churn_proba',
        color='churn_label',
        color_discrete_map={'Actif': '#2ecc71', 'Churné': '#e74c3c'},
        barmode='overlay', nbins=20, opacity=0.7
    )
    fig_churn.update_layout(
        **PLOT_LAYOUT,
        xaxis_title='Probabilité de Churn',
        yaxis_title='Nb Clients'
    )
    fig_churn.add_vline(
        x=0.5, line_dash='dash',
        line_color='white',
        annotation_text='Seuil 50%'
    )

    # FEATURE IMPORTANCE
    importances = pd.DataFrame({
        'feature':    X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance')
    fig_imp = px.bar(
        importances, x='importance', y='feature',
        orientation='h',
        color='importance',
        color_continuous_scale='Blues'
    )
    fig_imp.update_traces(
        texttemplate='%{x:.1%}', textposition='outside'
    )
    fig_imp.update_layout(
        **PLOT_LAYOUT,
        xaxis_title='Importance',
        yaxis_title='Feature',
        showlegend=False
    )

    # KMEANS SCATTER
    fig_km = px.scatter(
        dff, x='recency_days', y='monetary',
        color='cluster',
        symbol='rfm_segment',
        hover_name='customer_name',
        opacity=0.7,
        color_discrete_map={
            'VIP':       '#2ecc71',
            'Réguliers': '#3498db',
            'Inactifs':  '#e74c3c'
        }
    )
    fig_km.update_layout(
        **PLOT_LAYOUT,
        xaxis_title='Recency (jours)',
        yaxis_title='Monetary (USD)'
    )

    # TABLE
    dff_table = dff.copy()
    dff_table['churn_pct'] = (
        dff_table['churn_proba'] * 100
    ).round(1).astype(str) + '%'
    table_data = dff_table[[
        'customer_name', 'segment', 'region',
        'recency_days', 'frequency', 'monetary',
        'rfm_total', 'rfm_segment', 'churn_pct', 'cluster'
    ]].to_dict('records')

    stats_text = (
        f"📊 {len(dff)} clients affichés  |  "
        f"Revenue : ${dff['monetary'].sum():,.0f}  |  "
        f"Churn moyen : {dff['churn_proba'].mean()*100:.1f}%  |  "
        f"Monetary moyen : ${dff['monetary'].mean():,.0f}"
    )

    return (
        fig_pie, fig_rev, fig_bubble, fig_3d,
        fig_heatmap, fig_box, fig_churn, fig_imp,
        fig_km, table_data, stats_text
    )


# ============================================================
# 5. RUN
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, port=8050)
