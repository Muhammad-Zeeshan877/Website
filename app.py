import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Streamlit page config
st.set_page_config(page_title="MTTF Dashboard", layout="wide")

st.title("🚀 Machine MTTF Prediction Dashboard (Enhanced)")
st.markdown("Live monitoring of machine health with predictive analytics!")

# Autorefresh every 60 seconds
st_autorefresh(interval=60000, key="refresh")

# Database connection
def get_data():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=MDANIYAL-VM\\SQLEXPRESS;DATABASE=SQLTEST;Trusted_Connection=yes;'
    )
    query = "SELECT * FROM MTTF_Data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_data()

# KPI Metrics
st.subheader("📊 Key Metrics")
avg_mttf = round(df["MTTF (Years)"].mean(), 2)
at_risk_machines = df[df["Predicted MTTF (Years)"] < 6].shape[0]
total_machines = df.shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Average MTTF (Years)", f"{avg_mttf}")
col2.metric("Machines at Risk (< 6 Years)", f"{at_risk_machines}")
col3.metric("Total Machines", f"{total_machines}")

st.markdown("---")

# Filters Section
st.subheader("🔎 Filter Machines")

# Dropdown filter for Machine Type
machine_types = df['Machine Type'].unique()
selected_types = st.multiselect("Select Machine Types:", machine_types, default=machine_types)

# Filter DataFrame based on selection
filtered_df = df[df['Machine Type'].isin(selected_types)]

# Display Filtered Data
st.dataframe(filtered_df.style.background_gradient(cmap='Blues'))

st.markdown("---")

# Visualization Section
st.subheader("📈 Predicted MTTF by Machine Type")
fig = px.bar(
    filtered_df,
    x="Machine ID",
    y="Predicted MTTF (Years)",
    color="Machine Type",
    barmode="group",
    title="Predicted MTTF for Selected Machines"
)
st.plotly_chart(fig, use_container_width=True)

# Alerts for Critical Machines
st.subheader("⚠️ Machines at Critical Risk (Predicted MTTF < 5 Years)")
critical_df = filtered_df[filtered_df["Predicted MTTF (Years)"] < 5]

if not critical_df.empty:
    st.error("Critical machines detected! Immediate maintenance required! 🚨")
    st.dataframe(critical_df)
else:
    st.success("No critical machines at the moment. 👍")

# Download Button for CSV Export
st.subheader("⬇️ Download Report")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Machine MTTF Report as CSV",
    data=csv,
    file_name='MTTF_Report.csv',
    mime='text/csv'
)
