
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import streamlit as st

engine = create_engine('mssql://@RYAN/AdventureWorks2022?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')


QUERY = """
SELECT TOP 10 JobTitle, COUNT(*) AS Antal  
FROM HumanResources.Employee
GROUP BY JobTitle
ORDER BY Antal DESC;
"""

# Hämta data från databasen
with engine.connect() as connection:
    df = pd.read_sql(QUERY, connection)

# Unika jobbtitlar för filtrering
unique_titles = df['JobTitle'].unique()
selected_title = st.selectbox("Filter by Job Title", options=["All Titles"] + list(unique_titles), index=0)

# Filtrera data baserat på valt jobb
if selected_title == "All Titles":
    filtered_df = df
else:
    filtered_df = df[df['JobTitle'] == selected_title]

# Visa data som en tabell
st.dataframe(filtered_df.style.format({"Antal": "{:.0f}"}))

# Skapa ett stapeldiagram med Plotly
fig = px.bar(
    filtered_df,
    x="JobTitle",
    y="Antal",
    title="Antal per Job Title",
    labels={"JobTitle": "Job Title", "Antal": "Number of Employees"},
    color="JobTitle",
    barmode="group"
)

st.plotly_chart(fig)
