import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Streamlit page config
st.set_page_config(page_title="Sales Dashboard", layout="centered")

# Blue-themed custom background and styles
st.markdown("""
    <style>
        body {
            background-color: #e6f0ff;
            color: #003366;
        }
        .main {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 8px rgba(0, 51, 102, 0.2);
        }
        h1, h2 {
            color: #004080;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Container styling for main content
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # PostgreSQL connection string
    warehouse = "postgresql://sor_voc_warehouse_user:bGwVd60YuGe2yO4mWD3jbBlpRtGGe5Mj@dpg-d0lkq5hr0fns738fln5g-a.singapore-postgres.render.com/sor_voc_warehouse"
    engine = create_engine(warehouse, connect_args={"options": "-c client_encoding=utf8"})

    @st.cache_data
    def load_data():
        query = """
            SELECT "Product", COUNT(*) AS count
            FROM all_data
            GROUP BY "Product";
        """
        with engine.connect() as connection:
            result = connection.execute(text(query))
            return pd.DataFrame(result.mappings().all())

    # Load data
    df = load_data()

    # Title and Subheader
    st.title("Sales Dashboard 📊")
    st.subheader("🛍️ Top Products Bought by Customers")

    if not df.empty:
        fig = px.bar(
            df,
            x="Product",
            y="count",
            title="Most Bought Products",
            labels={"count": "Number of Purchases", "Product": "Product"},
            color="count",
            color_continuous_scale="Blues",
            text="count",
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(family="Arial", size=14, color="black"),
            yaxis=dict(title='Count', showgrid=True, gridcolor='LightGray'),
            xaxis=dict(title='Product'),
            title_x=0.5
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data found in the 'all_data' table.")

    st.markdown('</div>', unsafe_allow_html=True)
