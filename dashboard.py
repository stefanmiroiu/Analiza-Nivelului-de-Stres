import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Proiect", layout="wide")
st.title("Nivelul de stres al oamenilor în funcție de somn și timpul petrecut în fața ecranelor")

# ── Încărcare date ────────────────────────────────────────────────
fisier = st.file_uploader("Încarcă fișierul CSV", type=["csv"])

if fisier is None:
    st.info("Încarcă un fișier CSV pentru a continua.")
    st.stop()

df = pd.read_csv(fisier)

# ── FILTRE ──
st.sidebar.header("Filtre")

ocupatii = df["occupation"].unique().tolist()
ocupatii_selectate = st.sidebar.multiselect("Ocupații", ocupatii, default=ocupatii)

genuri = df['gender'].unique().tolist()
gen_selectat = st.sidebar.multiselect("Genuri", genuri, default=genuri)

df_filtrat = df[
    (df["occupation"].isin(ocupatii_selectate)) &
    (df["gender"].isin(gen_selectat))
]

# ── Statistici generale  ───────────────────
col1, col2, col3 , col4, col5= st.columns(5)
col1.metric("Ocupații", df_filtrat['occupation'].nunique())
col2.metric("Timp mediu petr. în fața ecranului", int(df_filtrat['daily_screen_time_hours'].mean()))
col3.metric("Cel mai mic scor al cal. somnului", df_filtrat['sleep_quality_score'].min())
col4.metric("Cel mai mare nivel de stres", df_filtrat['stress_level'].max())
col5.metric("Oboseala mentală medie", int(df_filtrat['mental_fatigue_score'].mean()))

# Tabelul
st.dataframe(df_filtrat.head(10), use_container_width=True)

# ── Grafic 1 — Plotly ────────────
st.subheader("Grafic 1")

fig = px.bar(
    df_filtrat.groupby("stress_level")["daily_screen_time_hours"].mean().reset_index(),
    x="stress_level",
    y="daily_screen_time_hours",
    color="stress_level",
    title="Nivelul de stres și timpul petrecut în fața unui ecran"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Grafic 2")

fig = px.bar(
    df_filtrat.groupby("notifications_received_per_day")["daily_screen_time_hours"].mean().reset_index(),
    x="notifications_received_per_day",
    y="daily_screen_time_hours",
    color="notifications_received_per_day",
    title="Notificările primite într-o zi și timpul petrecut în fața unui ecran"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Grafic 3")

fig = px.bar(
    df_filtrat.groupby("phone_usage_before_sleep_minutes")["sleep_quality_score"].mean().reset_index(),
    x="phone_usage_before_sleep_minutes",
    y="sleep_quality_score",
    color="phone_usage_before_sleep_minutes",
    title="Timpul petrecut în fața ecranului și calitatea somnului"
)
st.plotly_chart(fig, use_container_width=True)

# ── Grafic 2 — Matplotlib ──────────────────────
st.subheader("Grafic 4")

fig2, ax = plt.subplots(figsize=(9, 4))
ax.hist(df_filtrat["physical_activity_minutes"].dropna(), bins=20, color="#ff5c00", edgecolor="white")
ax.set_title("Distribuția timpului de activitate fizică")
ax.set_xlabel("Minute în care au făcut activitate fizică")
ax.set_ylabel("Frecvență")
st.pyplot(fig2)
plt.close(fig2)

st.subheader("Grafic 5")

fig2, ax = plt.subplots(figsize=(9, 4))
ax.hist(df_filtrat["mental_fatigue_score"].dropna(), bins=20, color="#ff5c00", edgecolor="white")
ax.set_title("Distribuția scorului de oboseală mentală")
ax.set_xlabel("Scorul de oboseală mentală")
ax.set_ylabel("Frecvență")
st.pyplot(fig2)

plt.close(fig2)

