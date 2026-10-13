"""Shared HerMetrics sidebar for Streamlit multipage projects."""
from pathlib import Path
import streamlit as st

PAGES = [
    ('app.py','Overview','📊'),
    ('pages/2_Ranking_Dashboard.py','Ranking','📈'),
    ('pages/3_Bank_Profile.py','Bank Profile','🏦'),
    ('pages/4_Bank_Comparison.py','Bank Comparison','⚖️'),
    ('pages/1_Evidence_Explorer.py','Evidence Explorer','🔎'),
    ('pages/5_Scoring_Evidence_Audit.py','Scoring Audit','📋'),
    ('pages/6_Data_Validation.py','Data Validation','✅'),
]
CSS = '''<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&family=Playfair+Display:wght@700;800&display=swap');
[data-testid="stSidebar"], [data-testid="stSidebarContent"]{background:#fffdf9!important;}
[data-testid="stSidebar"]{border-right:1px solid #e8dfe0!important;}
[data-testid="stSidebarNav"]{display:none!important;}
.hm-global-brand{font:800 34px/1.18 'Playfair Display',Georgia,serif;color:#790c34;margin:12px 0 4px;white-space:nowrap;}
.hm-global-caption{font:800 10px 'Be Vietnam Pro',sans-serif;letter-spacing:1.4px;color:#790c34;margin-bottom:28px;}
.hm-global-workspace{font:800 12px 'Be Vietnam Pro',sans-serif;letter-spacing:1.3px;color:#85616f;margin-bottom:12px;}
[data-testid="stSidebar"] [data-testid="stPageLink"] a{border-radius:11px!important;padding:10px 11px!important;margin:2px 0!important;min-height:42px!important;text-decoration:none!important;}
[data-testid="stSidebar"] [data-testid="stPageLink"] a p,[data-testid="stSidebar"] [data-testid="stPageLink"] a span{font-family:'Be Vietnam Pro',Arial,sans-serif!important;font-weight:800!important;font-size:14px!important;color:#790c34!important;}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{background:#f3eaed!important;}
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"], [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-selected="true"]{background:#eceff1!important;}
</style>'''

def render(root: Path, *, show_nav: bool = True):
    st.markdown(CSS, unsafe_allow_html=True)
    if not show_nav:
        return
    with st.sidebar:
        st.markdown('<div class="hm-global-brand">HerMetrics</div><div class="hm-global-caption">BANKING INTELLIGENCE</div><div class="hm-global-workspace">WORKSPACE</div>',unsafe_allow_html=True)
        for relative,label,icon in PAGES:
            if (root / relative).is_file():
                st.page_link(relative,label=label,icon=icon)
