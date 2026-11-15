import streamlit as st
import pandas as pd
import unicodedata

st.markdown("""
<div style='text-align:center; margin-bottom:10px;'>
    <svg width="75" height="50" viewBox="0 0 900 600" style="border-radius:4px; box-shadow:0 2px 5px rgba(0,0,0,0.2);">
        <rect width="300" height="600" fill="#00853f"/>
        <rect x="300" width="300" height="600" fill="#fdef42"/>
        <rect x="600" width="300" height="600" fill="#e31b23"/>
        <polygon points="450,200 479,291 575,291 497,347 527,438 450,382 373,438 403,347 325,291 421,291" fill="#00853f"/>
    </svg>
</div>
<h1 style='text-align:center; color:#008543; margin-top:0;'>ASSOS NDAYANE VILLAGE</h1>
<p style='text-align:center; color:#E31B23; font-weight:bold;'>Tableau de Bord Général & Suivi des Cotisations</p><hr>
""", unsafe_allow_html=True)

#st.markdown("<div style='text-align:center; margin-bottom:10px;'><img src='https://flagcdn.com' width='65'></div>", unsafe_allow_html=True)
#st.markdown("<h1 style='text-align:center; color:#008543; margin-top:0;'>ASSOS NDAYANE VILLAGE</h1><p style='text-align:center; color:#E31B23; font-weight:bold;'>Tableau de Bord Général & Suivi des Cotisations</p><hr>", unsafe_allow_html=True)

def net(t):
    return '' if pd.isna(t) else ''.join(c for c in unicodedata.normalize('NFD', str(t).strip().title()) if unicodedata.category(c) != 'Mn')

df = pd.read_csv("cotisations.csv")
df.columns = df.columns.str.strip()
df['Date'] = df['Date'].fillna('Inconnu').astype(str).str.strip().str.lower()
df['Résidence'] = df['Résidence'].fillna('Non spécifiée').astype(str).str.strip().replace('', 'Non spécifiée')
df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
df['Nom Complet'] = (df['Nom'].apply(net) + " " + df['Prénom'].apply(net)).str.strip()
df = df[df['Nom Complet'].str.len() > 2]

try:
    df_dep = pd.read_csv("depenses.csv")
    df_dep.columns = df_dep.columns.str.strip()
    df_dep['Date'] = df_dep['Date'].fillna('Inconnu').astype(str).str.strip().str.lower()
    # Nettoyage automatique de la colonne Enveloppe (supprime les espaces, accents et harmonise les majuscules)
    df_dep['Enveloppe'] = df_dep['Enveloppe'].apply(net)
    df_dep['Montant Sorti'] = pd.to_numeric(df_dep['Montant Sorti'], errors='coerce').fillna(0)
except:
    df_dep = pd.DataFrame(columns=['Date', 'Enveloppe', 'Montant Sorti', 'Motif'])

st.info("📜 **Règles des Sages :** Adhésion : 1 000 F • **Social Fixe : 25 000 F** (62,5% Santé/Accidents • 37,5% Sinistres/Village) • Décès exclu • Retard 3 mois : Avertissement | +6 mois : Radiation")

mois = st.selectbox("📅 Période (Mois) :", ["Tous les mois"] + list(df['Date'].unique()))
res = st.selectbox("🏘️ Quartier / Résidence :", ["Toutes les résidences"] + sorted(list(df['Résidence'].unique())))

df_f = df if mois == "Tous les mois" else df[df['Date'] == mois]
dep_f = df_dep if mois == "Tous les mois" else df_dep[df_dep['Date'] == mois]
if res != "Toutes les résidences":
    df_f = df_f[df_f['Résidence'] == res]

# Calculs globaux
tot_rec = int(df_f['Montant FCFA'].sum())
tot_dep = int(dep_f['Montant Sorti'].sum())
d_dev = int(dep_f[dep_f['Enveloppe'] == 'Developpement']['Montant Sorti'].sum()) if not dep_f.empty else 0
d_san = int(dep_f[dep_f['Enveloppe'] == 'Sante']['Montant Sorti'].sum()) if not dep_f.empty else 0
d_sin = int(dep_f[dep_f['Enveloppe'] == 'Sinistres']['Montant Sorti'].sum()) if not dep_f.empty else 0

env_soc = min(tot_rec, 25000)
f_dev = max(0, tot_rec - env_soc)
f_san = int(env_soc * 0.625)
f_sin = env_soc - f_san

t1, t2, t3 = st.tabs(["💰 RECETTES", "📤 DÉPENSES", "🏦 RESTE DE LA CAISSE"])

with t1:
    nb_tot = len(df_f)
    nb_ok = int((df_f['Montant FCFA'] >= 1000).sum())
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card'><b>TOTAL COLLECTÉ</b><div class='kpi-val'>{tot_rec:,} F</div><small>Sur {nb_tot*1000:,} F</small></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card' style='border-color:#E31B23;'><b>RESTE À RECOUVRIR</b><div class='kpi-val' style='color:#E31B23;'>{max(0, nb_tot*1000 - tot_rec):,} F</div><small>{nb_tot - nb_ok} en attente</small></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card' style='border-color:#FDEF42;'><b>PARTICIPATION</b><div class='kpi-val'>{int(nb_ok/nb_tot*100) if nb_tot else 0} %</div><small>{nb_ok} / {nb_tot} cotisations</small></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><b>BUDGET SOCIAL FIXE</b><div class='kpi-val'>{env_soc:,} F</div><small>Plafond fixe</small></div>", unsafe_allow_html=True)

    st.subheader("🏦 Répartition (Base Sociale Fixe de 25 000 F)")
    f1, f2, f3 = st.columns(3)
    f1.metric("🏗️ Développement (Le Reste)", f"{f_dev:,} FCFA")
    f2.metric("🩺 Santé & Accidents (62,5%)", f"{f_san:,} FCFA")
    f3.metric("🌪️ Sinistres & Village (37,5%)", f"{f_sin:,} FCFA")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("🏘️ Par Résidence")
        st.bar_chart(df_f.groupby('Résidence')['Montant FCFA'].sum(), color="#008543")
    with g2:
        st.subheader("⚖️ Statuts (Comité des Sages)")
        m_tot = df['Date'].nunique()
        pay = df[df['Montant FCFA'] >= 1000].groupby('Nom Complet')['Date'].nunique()
        st_df = df[['Nom Complet', 'Résidence']].drop_duplicates('Nom Complet')
        st_df['Imp'] = (m_tot - st_df['Nom Complet'].map(pay).fillna(0).astype(int)).clip(0)
        st_df['Statut'] = st_df['Imp'].apply(lambda x: "🔴 Radié (+6m)" if x >= 6 else ("🟠 Avert. (3-5m)" if x >= 3 else (f"🟡 Retard ({x}m)" if x > 0 else "🟢 À jour")))
        if res != "Toutes les résidences": st_df = st_df[st_df['Résidence'] == res]
        st.dataframe(st_df[['Nom Complet', 'Résidence', 'Statut']], use_container_width=True, height=250)

    st.subheader("📋 Registre des Cotisations")
    st.dataframe(df_f[['Date', 'Nom Complet', 'Résidence', 'Montant FCFA', 'Mode paiement']], use_container_width=True)

with t2:
    d1, d2, d3, d4 = st.columns(4)
    d1.markdown(f"<div class='kpi-card' style='border-color:#E31B23;'><b>TOTAL DÉPENSÉ</b><div class='kpi-val' style='color:#E31B23;'>{tot_dep:,} F</div></div>", unsafe_allow_html=True)
    d2.markdown(f"<div class='kpi-card'><b>DÉP. DÉVELOPPEMENT</b><div class='kpi-val'>{d_dev:,} F</div></div>", unsafe_allow_html=True)
    d3.markdown(f"<div class='kpi-card'><b>DÉP. SANTÉ</b><div class='kpi-val'>{d_san:,} F</div></div>", unsafe_allow_html=True)
    d4.markdown(f"<div class='kpi-card'><b>DÉP. SINISTRES</b><div class='kpi-val'>{d_sin:,} F</div></div>", unsafe_allow_html=True)
    
    if not dep_f.empty:
        st.dataframe(dep_f, use_container_width=True)
    else:
        st.info("Aucune dépense enregistrée.")

with t3:
    df_m = df if mois == "Tous les mois" else df[df['Date'] == mois]
    rg = int(df_m['Montant FCFA'].sum())
    es = min(rg, 25000)
    rd, rsa, rsi = max(0, rg - es), int(es * 0.625), es - int(es * 0.625)

    r1, r2, r3, r4 = st.columns(4)
    r1.markdown(f"<div class='kpi-card'><b>RESTE GLOBAL</b><div class='kpi-val'>{rg - tot_dep:,} F</div></div>", unsafe_allow_html=True)
    r2.markdown(f"<div class='kpi-card'><b>RESTE DÉVELOPPEMENT</b><div class='kpi-val'>{rd - d_dev:,} F</div></div>", unsafe_allow_html=True)
    r3.markdown(f"<div class='kpi-card'><b>RESTE SANTÉ</b><div class='kpi-val'>{rsa - d_san:,} F</div></div>", unsafe_allow_html=True)
    r4.markdown(f"<div class='kpi-card'><b>RESTE SINISTRES</b><div class='kpi-val'>{rsi - d_sin:,} F</div></div>", unsafe_allow_html=True)

    st.table(pd.DataFrame({
        "Enveloppe": ["🏗️ Développement", "🩺 Santé (62,5% des 25k)", "🌪️ Sinistres (37,5% des 25k)", "💰 TOTAL"],
        "Recettes": [f"{rd:,} F", f"{rsa:,} F", f"{rsi:,} F", f"{rg:,} F"],
        "Dépenses": [f"{d_dev:,} F", f"{d_san:,} F", f"{d_sin:,} F", f"{tot_dep:,} F"],
        "Reste en Caisse": [f"{rd - d_dev:,} F", f"{rsa - d_san:,} F", f"{rsi - d_sin:,} F", f"{rg - tot_dep:,} F"]
    }))

st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>ASSOS NDAYANE VILLAGE — Commune de Tocky Gare, Diourbel</p>", unsafe_allow_html=True)
