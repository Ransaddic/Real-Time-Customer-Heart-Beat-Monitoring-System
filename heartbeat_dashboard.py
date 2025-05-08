import streamlit as st
from streamlit_autorefresh import st_autorefresh
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Heart Rate Monitor", page_icon="❤️", layout="wide")
st.title("📈 Real-Time Customer Heart Rate Monitor")

# PostgreSQL connection (no caching)
def get_connection():
    return psycopg2.connect(
        dbname='heart_monitor',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5433'
    )

# Load data
@st.cache_data(ttl=5)
def load_data():
    with get_connection() as conn:
        query = """
            SELECT customer_id, timestamp, heart_rate
            FROM heartbeat_data
            ORDER BY timestamp DESC
            LIMIT 100
        """
        return pd.read_sql_query(query, conn)

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="heartbeat_refresh")

# Load data
df = load_data()
if df.empty:
    st.warning("No data available yet.")
    st.stop()

# Sidebar
st.sidebar.header("🔍 Filters")
selected_customer = st.sidebar.selectbox("Select Customer", df['customer_id'].unique())
st.sidebar.caption(f"Total Records: {len(df)}")

# Filter by customer
customer_data = df[df['customer_id'] == selected_customer].sort_values(by="timestamp")

# Summary stats
st.markdown(f"### 📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Mean BPM", f"{customer_data['heart_rate'].mean():.2f}")
col2.metric("Min BPM", f"{customer_data['heart_rate'].min()}")
col3.metric("Max BPM", f"{customer_data['heart_rate'].max()}")

# Plot
st.markdown("### 📈 Heart Rate Trend")
fig = px.line(
    customer_data,
    x="timestamp",
    y="heart_rate",
    color_discrete_sequence=["#EF553B"],
    markers=True
)
fig.update_layout(
    xaxis_title="Timestamp",
    yaxis_title="Heart Rate (bpm)",
    height=450
)
st.plotly_chart(fig, use_container_width=True)

# Table
st.markdown("### 📋 Heart Rate Data Table (Latest 100 Records)")
customer_data['timestamp'] = customer_data['timestamp'].astype(str)  # Ensure timestamp is string
table_fig = go.Figure(data=[go.Table(
    header=dict(values=list(customer_data.columns), fill_color='#2C3E50', font=dict(color='white'), align='left'),
    cells=dict(values=[customer_data[col] for col in customer_data.columns], fill_color='lavender', align='left')
)])
table_fig.update_layout(height=400)
st.plotly_chart(table_fig, use_container_width=True)
