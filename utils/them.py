
import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* Nền chính */
    .stApp {
        background-color: #FFF8FB;
    }

    /* Thanh điều hướng */
    [data-testid="stSidebar"] {
        background-color: #FCEAF2;
    }

    /* Tiêu đề */
    h1, h2, h3 {
        color: #AD1457;
        font-weight: 700;
    }

    /* Chữ */
    p, label {
        line-height: 1.6;
    }

    /* KPI */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 16px;
        border: 1px solid #F4DCE7;
        border-radius: 12px;
    }

    /* Bộ lọc */
    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"] {
        border-radius: 10px;
    }

    /* Bảng */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Nút */
    .stButton > button {
        background-color: #AD1457;
        color: white;
        border-radius: 10px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #880E4F;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
