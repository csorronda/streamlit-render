import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Streamlit page config
st.set_page_config(page_title="Sales Dashboard", layout="centered")

st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #d6f0ff; /* Baby blue background */
            color: #222222;
        }
        .main {
            background-color: #f0f8ff; /* light pastel blue instead of white */
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 16px rgba(173, 216, 230, 0.4);
        }
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
            color: #1a1a1a; /* Darker title color */
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
            FROM sales_data
            GROUP BY "Product";
        """
        with engine.connect() as connection:
            result = connection.execute(text(query))
            return pd.DataFrame(result.mappings().all())

    # Load data
    df = load_data()

    # Title and Subheader
    st.title("🌈 Sales Dashboard")
    st.subheader("🦋 Most Loved Products by Our Customers 🦋")

    if not df.empty:
        # Custom gradient from baby blue to baby pink
        fig = px.bar(
            df,
            x="Product",
            y="count",
            title="Most Popular Products by Purchases",
            labels={"count": "Number of Purchases", "Product": "Product"},
            color="count",
            color_continuous_scale=[[0, '#89CFF0'], [1, '#FFB6C1']],
            text="count",
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            title_font=dict(size=22, color='#000000'),
            font=dict(family="Comic Sans MS, Arial", size=14, color="#000000"),
            plot_bgcolor='#d6f0ff',     # Match background color
            paper_bgcolor='#d6f0ff',    # Match background color
            xaxis_tickangle=-45,
            xaxis=dict(title='Product', color='#000000'),
            yaxis=dict(title='Count', color='#000000', showgrid=True, gridcolor='Black'),
            title_x=0.5
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data found in the 'sales_data' table.")

    st.markdown('</div>', unsafe_allow_html=True)
