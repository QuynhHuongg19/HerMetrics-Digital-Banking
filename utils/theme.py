
import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* Font và màu nền */
    .stApp {
        background: linear-gradient(
            145deg,
            #FFF9FC 0%,
            #FFFFFF 48%,
            #FFF0F6 100%
        );
        color: #302438;
    }

    /* Khu vực nội dung */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #FFF0F7 0%,
            #FCE2ED 100%
        );
        border-right: 1px solid #F3D3E2;
    }

    [data-testid="stSidebar"] a {
        border-radius: 10px;
        transition: 0.2s ease;
    }

    [data-testid="stSidebar"] a:hover {
        background: #F9D5E5;
    }

    /* Tiêu đề */
    h1 {
        color: #8D174E !important;
        font-size: 2.35rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px;
    }

    h2 {
        color: #9D235C !important;
        font-weight: 750 !important;
        margin-top: 1.4rem;
    }

    h3 {
        color: #AE3A70 !important;
        font-weight: 700 !important;
    }

    /* KPI Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(
            135deg,
            #FFFFFF,
            #FFF0F7
        );
        padding: 22px 20px;
        border: 1px solid #F2D6E4;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(173, 20, 87, 0.07);
        transition: transform 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(173, 20, 87, 0.12);
    }

    [data-testid="stMetricLabel"] {
        color: #93627B;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #A01557;
        font-size: 2rem;
        font-weight: 800;
    }

    /* Biểu đồ Plotly */
    [data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #F4E2EA;
        border-radius: 18px;
        padding: 10px;
        box-shadow: 0 5px 18px rgba(70, 35, 55, 0.04);
        overflow: hidden;
    }

    /* Bảng dữ liệu */
    [data-testid="stDataFrame"] {
        border: 1px solid #F0D9E4;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(70, 35, 55, 0.04);
    }

    /* Nút bấm */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(
            90deg,
            #B61E65,
            #DB669A
        );
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 650;
        padding: 0.55rem 1.2rem;
        box-shadow: 0 4px 12px rgba(173, 20, 87, 0.12);
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #93164E;
        color: white;
        border: none;
    }

    /* Bộ lọc */
    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"] {
        border-radius: 12px;
    }

    /* Tab */
    button[data-baseweb="tab"] {
        font-weight: 650;
        border-radius: 8px;
    }

    /* Đường phân cách */
    hr {
        border-color: #F1DCE6;
    }

    /* Caption */
    [data-testid="stCaptionContainer"] {
        color: #8F7582;
    }

    </style>
    """, unsafe_allow_html=True)
