import streamlit as st

import pandas as pd

import plotly.graph_objects as go

import plotly.express as px

from pathlib import Path

from html import escape
import base64
import mimetypes



st.set_page_config(page_title='HerMetrics | Banking Intelligence', page_icon='📊', layout='wide', initial_sidebar_state='expanded')



ROOT = Path(__file__).resolve().parent

DATA = ROOT / 'data'

LOGOS = ROOT / 'assets' / 'logos'
ART = ROOT / 'assets' / 'vietnam_art'

def art_uri(name):
    """Return local artwork as a CSS-safe data URL; gracefully handle missing images."""
    path = ART / name
    if not path.is_file():
        return ''
    mime = mimetypes.guess_type(path.name)[0] or 'image/png'
    return f'data:{mime};base64,{base64.b64encode(path.read_bytes()).decode("ascii")}'


BANKS = ['BIDV', 'MB', 'OCB', 'VCB', 'VietinBank']

BANK_COLORS = {'BIDV':'#D6A92C','MB':'#315BD4','OCB':'#9EBB38','VCB':'#138B6E','VietinBank':'#69A9D8'}

PILLARS = {'A':'Chiến lược & nguồn lực số','B':'Sản phẩm số & trải nghiệm khách hàng','C':'Công nghệ & dữ liệu','D':'Vận hành số & an toàn'}

PILLAR_COLORS = {'A':'#741B3B','B':'#B94C70','C':'#DC879E','D':'#E9B9C7'}

CRITERIA = [f'{p}{i}' for p in 'ABCD' for i in range(1,5)]



st.markdown('''<style>

:root{--wine:#681c38;--rose:#b85577;--ink:#263044;--line:#ece7eb}

.stApp{background:#f9f8fa;color:var(--ink)}

.block-container{max-width:1600px;padding:1.4rem 2rem 3rem}

[data-testid="stSidebar"]{background:linear-gradient(165deg,#fff 5%,#fff7fa 70%,#f5e8ef 100%);border-right:1px solid #eadfe5}

[data-testid="stSidebar"] .block-container{padding-top:1.5rem}

[data-testid="stSidebarNav"]{display:none!important}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding-top:1.0rem}

[data-testid="stSidebar"] .stPageLink a{padding:10px 13px;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px}

[data-testid="stSidebar"] .stPageLink a:hover{background:#f6e7ee}

[data-testid="stSidebar"] .stPageLink a[aria-current="page"]{background:#f1dce6;color:#671a38}

[data-testid="stSidebar"] .stPageLink{margin-bottom:3px}

.hm-nav-title{font-size:10px;letter-spacing:2px;font-weight:750;color:#927887;margin:12px 0 10px}



[data-testid="stSidebarNav"] a:hover{background:#f4e3eb}

[data-testid="stSidebarNav"] a[aria-current="page"]{background:#f3dce5;color:#661a37}

h1,h2,h3{color:#321d2b!important;letter-spacing:-.5px}

.hm-brand{font-family:Georgia,serif;font-size:39px;letter-spacing:-1.8px;color:#741b3b;line-height:1.2;margin-bottom:3px}

.hm-brand-small{font-size:9px;letter-spacing:2.5px;color:#8a7280;margin-bottom:23px}

.hm-eyebrow{font-size:11px;letter-spacing:3px;font-weight:700;color:#667084;margin-bottom:10px}

.hm-title{font-family:Georgia,'Times New Roman',serif;font-size:clamp(32px,3.3vw,55px);font-weight:600;letter-spacing:-1.5px;line-height:1.08;color:#1e283a;margin-bottom:12px}

.hm-sub{font-size:14px;color:#697588;line-height:1.6;max-width:950px}

.hm-hero{padding:28px 28px 32px;position:relative;overflow:hidden;min-height:235px;border-radius:20px;background:linear-gradient(110deg,#57152f,#a65075 72%,#f6e4eb);box-shadow:0 6px 24px rgba(88,40,60,.055);border:1px solid #f1e5eb;margin-bottom:18px}

.hm-hero .hm-title,.hm-hero .hm-sub,.hm-hero .hm-eyebrow{position:relative;z-index:1}

.hm-hero .hm-sub{max-width:610px;font-size:15px}

.hm-hero .hm-title{font-size:clamp(36px,3.5vw,56px)}



.hm-hero:after{display:none}

.hm-section{font-size:23px;font-weight:750;letter-spacing:-.4px;color:#2c2936;margin:28px 0 15px}

.hm-card{border:1px solid rgba(116,27,59,.09);border-radius:16px;padding:23px 22px;box-shadow:0 6px 18px rgba(45,26,39,.055);height:100%;transition:transform .2s ease,box-shadow .2s ease}
.hm-card:hover{transform:translateY(-3px);box-shadow:0 11px 24px rgba(45,26,39,.11)}
/* HerMetrics monochromatic ombre: burgundy -> dusty rose -> blush */
.hm-card.kpi-1{background:linear-gradient(125deg,#F2CEDD 0%,#FBEAF1 57%,#FFF9FC 100%)}
.hm-card.kpi-2{background:linear-gradient(125deg,#EAC1D2 0%,#F8E3EC 57%,#FFF7FA 100%)}
.hm-card.kpi-3{background:linear-gradient(125deg,#DFA8BF 0%,#F4D7E3 57%,#FFF4F8 100%)}
.hm-card.kpi-4{background:linear-gradient(125deg,#D9A1B9 0%,#F1CEDD 57%,#FFF1F7 100%)}
.hm-card.kpi-1 .hm-k-num,.hm-card.kpi-2 .hm-k-num,
.hm-card.kpi-3 .hm-k-num,.hm-card.kpi-4 .hm-k-num{color:#741B3B}
.hm-card .hm-k-label{color:#63384B;font-weight:650}
.hm-card .hm-k-note{color:#815B6C}
.hm-hero{border-color:#E9C9D6;box-shadow:0 8px 24px rgba(116,27,59,.09)}

.hm-k-label{font-size:12px;color:#7b7d8a;margin-top:4px}.hm-k-num{font-family:Georgia,serif;color:#741b3b;font-size:36px;line-height:1.2}.hm-k-note{font-size:11px;color:#9b96a1;margin-top:8px}

.hm-note{font-size:12px;color:#805569;background:#fcf1f6;border-left:3px solid #b95679;padding:11px 14px;border-radius:0 8px 8px 0;margin-top:13px}

.hm-heading{font-family:Georgia,serif;font-size:19px;font-weight:700;color:#2b2631;margin-bottom:8px}

.hm-table{width:100%;border-collapse:collapse;font-size:13px}.hm-table td,.hm-table th{padding:11px 6px;border-bottom:1px solid #f0edf0;text-align:left}.hm-table th{font-size:11px;color:#8b8791;font-weight:600}.hm-bar{height:12px;border-radius:6px;background:linear-gradient(90deg,#d48da5,#741b3b)}

[data-testid="stVerticalBlockBorderWrapper"]{background:#fff;border-color:#ebe6ea!important;border-radius:14px!important;box-shadow:0 4px 14px rgba(45,26,39,.035)}

[data-testid="stPlotlyChart"]{border:none!important;box-shadow:none!important;background:transparent!important;padding:0!important}

[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden}

[data-testid="stMetric"]{background:white;border:1px solid #eee7ec;border-radius:12px;padding:13px}

.stButton>button,.stDownloadButton>button{background:#741b3b;color:white;border:0;border-radius:9px}

.stButton>button:hover,.stDownloadButton>button:hover{background:#9e3c60;color:white}


/* HerMetrics interactive navigation and controls — original hero retained */
[data-testid="stSidebar"] { min-width: 280px !important; width: 280px !important; }
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-left: 18px !important; padding-right: 18px !important; }
[data-testid="stSidebar"] .hm-brand { font-size: 35px !important; white-space: nowrap; letter-spacing: -1.6px; }
[data-testid="stSidebar"] .stPageLink { width: 100%; margin: 3px 0 !important; }
[data-testid="stSidebar"] .stPageLink a,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
  display: flex !important; align-items: center; gap: 9px;
  width: 100%; min-height: 43px; padding: 10px 13px !important;
  border-radius: 10px !important; border-left: 3px solid transparent;
  color: #475066 !important; font-size: 13px !important;
  font-weight: 600 !important; line-height: 1.35 !important;
  transition: background .18s ease, color .18s ease, border-color .18s ease, transform .18s ease;
}
[data-testid="stSidebar"] .stPageLink a:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
  background: #f3dce6 !important; color: #681c38 !important;
  border-left-color: #b85577 !important; transform: translateX(2px);
}
[data-testid="stSidebar"] .stPageLink a[aria-current="page"],
[data-testid="stSidebar"] .stPageLink a[aria-current="true"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="true"],
[data-testid="stSidebar"] .stPageLink:has([aria-current="page"]) a,
[data-testid="stSidebar"] .stPageLink:has([aria-current="true"]) a {
  background: #741b3b !important; color: #fff !important;
  border-left-color: #e5b0c3 !important;
  box-shadow: 0 3px 10px rgba(116,27,59,.14);
}
[data-testid="stSidebar"] .stPageLink a[aria-current] *,
[data-testid="stSidebar"] .stPageLink:has([aria-current]) a * { color: inherit !important; }
/* Multiselect: replace bright red selected tags with muted rose */
span[data-baseweb="tag"] { background: #f3e2ea !important; color: #681c38 !important;
  border: 1px solid #e7cad6 !important; border-radius: 7px !important; }
span[data-baseweb="tag"] span, span[data-baseweb="tag"] svg { color: #681c38 !important; fill: #681c38 !important; }
[data-baseweb="select"] > div, [data-baseweb="input"] > div {
  background: #fff !important; border: 1px solid #e8dce3 !important;
  border-radius: 10px !important; min-height: 41px;
  transition: border-color .18s ease, box-shadow .18s ease;
}
[data-baseweb="select"] > div:hover, [data-baseweb="input"] > div:hover { border-color: #b85577 !important; }
[data-baseweb="select"] > div:focus-within, [data-baseweb="input"] > div:focus-within {
  border-color: #8e3154 !important; box-shadow: 0 0 0 3px rgba(184,85,119,.12) !important;
}
[data-testid="stTextInput"] input { color: #263044 !important; font-size: 14px !important; }
[data-testid="stTextInput"] input::placeholder { color: #9c95a0 !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #584658 !important; font-weight: 650 !important; font-size: 12px !important; }
[data-testid="stSidebar"] [data-baseweb="select"] { margin-bottom: 3px; }
/* Improve button hover while leaving all charts and KPI styling untouched */
.stButton > button, .stDownloadButton > button { transition: background .18s ease, box-shadow .18s ease, transform .18s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { box-shadow: 0 4px 12px rgba(116,27,59,.16); transform: translateY(-1px); }


/* Prominent website brand inside hero; readable on burgundy overlay */
.hm-hero .hm-site-name{position:relative;z-index:2;display:inline-block;font-family:Georgia,'Times New Roman',serif;font-size:25px;font-weight:700;letter-spacing:-.6px;color:#FFFFFF !important;margin-bottom:12px;text-shadow:0 2px 10px rgba(50,12,30,.35)}
.hm-hero .hm-title{max-width:650px}
/* HERO TITLE: ombre wine-to-rose overlay, keep building image */
.hm-hero .hm-title { color:#FFFFFF !important; text-shadow:0 2px 10px rgba(65,16,38,.16); }
.hm-hero .hm-eyebrow { color:#FCE5EF !important; }
.hm-hero .hm-sub { color:#FFF1F6 !important; }
.hm-hero { border-color:#DCA9BF !important; }

/* HerMetrics readability upgrade: typography only, preserve layout and colors */
html, body, [data-testid="stAppViewContainer"] {font-size:17px !important;}
.hm-hero .hm-site-name{font-size:31px !important;}
.hm-hero .hm-eyebrow{font-size:13px !important;letter-spacing:2.1px;}
.hm-hero .hm-title{font-size:clamp(40px,3.9vw,62px) !important;line-height:1.12;}
.hm-hero .hm-sub{font-size:17px !important;line-height:1.65;}
.hm-brand{font-size:42px !important;}
[data-testid="stSidebar"] .hm-brand{font-size:40px !important;}
.hm-brand-small{font-size:11px !important;}
.hm-nav-title{font-size:12px !important;}
[data-testid="stSidebar"] .stPageLink a{font-size:16px !important;}
.hm-section{font-size:27px !important;}
.hm-heading{font-size:22px !important;}
.hm-k-num{font-size:42px !important;}
.hm-k-label{font-size:15px !important;}
.hm-k-note{font-size:13px !important;line-height:1.5;}
.hm-note{font-size:14px !important;line-height:1.65;}
.hm-table{font-size:15px !important;}
.hm-table th{font-size:13px !important;}
.hm-table td,.hm-table th{padding:13px 8px !important;}
[data-testid="stTextInput"] input{font-size:16px !important;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-size:14px !important;}
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p{font-size:15px;line-height:1.6;}
[data-testid="stSelectbox"] *,[data-testid="stMultiSelect"] *,[data-testid="stRadio"] label{font-size:15px;}
[data-testid="stDataFrame"]{font-size:15px;}
@media(max-width:900px){.hm-hero .hm-title{font-size:clamp(32px,6vw,46px) !important}.hm-hero .hm-site-name{font-size:26px !important}.hm-k-num{font-size:35px !important}}
</style>''', unsafe_allow_html=True)



# Vietnam Art Edition: pure white background, real local landscape images, no floral ornaments.
hero_image = art_uri('ho_guom_hoa_sen.png')
side_image = art_uri('pho_co_mua_thu.png')
landscape_image = art_uri('ruong_bac_thang.png')

st.markdown(f"""<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{background:#fff!important}}
.block-container{{max-width:1750px;padding:0.65rem 1.25rem 3rem!important}}
[data-testid="stSidebar"]{{background:#fff!important;border-right:1px solid #eee7eb!important;min-width:310px!important;width:310px!important;max-width:310px!important;flex:0 0 310px!important}}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{{padding:1.2rem 22px!important}}
.hm-brand{{font:700 39px Georgia,serif!important;letter-spacing:-1.5px;color:#821033!important;text-align:center;margin:12px 0 0}}
.hm-brand-small{{font-size:10px!important;text-align:center;letter-spacing:2px;color:#8c2143!important;margin-bottom:17px}}
.hm-sidebar-art{{height:290px;border-radius:13px;margin:15px 0;background:url('{side_image}') center/cover no-repeat;box-shadow:0 3px 12px #6d284019}}
[data-testid="stSidebar"] .stPageLink a{{font:600 15px Georgia,serif!important;color:#801333!important;border-radius:12px!important;min-height:45px!important}}
[data-testid="stSidebar"] .stPageLink a:hover{{background:#f8e6ed!important}}
[data-testid="stSidebar"] .stPageLink a[aria-current="page"]{{background:linear-gradient(100deg,#87002f,#ca879e)!important;color:white!important}}
.hm-hero{{min-height:310px!important;padding:34px 42px!important;border-radius:17px!important;background:linear-gradient(90deg,rgba(255,255,255,.88) 0%,rgba(255,255,255,.67) 25%,rgba(255,255,255,.09) 53%,rgba(255,255,255,0) 72%),url('{hero_image}') center/cover no-repeat!important;border:1px solid #eee5e8!important;box-shadow:0 4px 16px #5c18301a!important}}
.hm-hero .hm-site-name{{font:700 clamp(40px,4.4vw,70px) Georgia,serif!important;color:#820c35!important;text-shadow:none!important;line-height:1.05;margin-bottom:2px!important}}
.hm-hero .hm-title{{font:700 clamp(32px,3.3vw,49px) Georgia,serif!important;line-height:1.05!important;max-width:590px!important;color:#820c35!important;text-shadow:none!important;margin:0 0 8px!important}}
.hm-hero .hm-eyebrow{{font-size:11px!important;color:#8a2445!important;letter-spacing:3px!important;margin:5px 0!important}}
.hm-hero .hm-sub{{font:16px/1.5 Georgia,serif!important;color:#263044!important;max-width:480px!important}}
.hm-card{{min-height:175px!important;padding:21px 20px!important;border-radius:14px!important;border:1px solid #eee2e6!important;box-shadow:0 4px 13px #6a263013!important;background-size:cover!important;background-position:center!important}}
.hm-card.kpi-1{{background-image:linear-gradient(90deg,#fffafbd9,#fff9f51a),url('{art_uri('chua_mot_cot.png')}')!important}}
.hm-card.kpi-2{{background-image:linear-gradient(90deg,#fffafbd9,#fff9f51a),url('{art_uri('ruong_bac_thang.png')}')!important}}
.hm-card.kpi-3{{background-image:linear-gradient(90deg,#fffafbd9,#fff9f51a),url('{art_uri('lang_que_viet_nam.png')}')!important}}
.hm-card.kpi-4{{background-image:linear-gradient(90deg,#fffafbd9,#fff9f51a),url('{art_uri('pho_co_mua_thu.png')}')!important}}
.hm-k-num{{font:700 41px Georgia,serif!important;color:#850b35!important}}
.hm-k-label{{font:700 16px Georgia,serif!important;color:#51223a!important}}
.hm-k-note{{font-size:12px!important;color:#72515e!important}}
.hm-section{{font:700 24px Georgia,serif!important;color:#7e0c33!important;margin:19px 0 10px!important}}
.hm-heading{{font:700 21px Georgia,serif!important;color:#7e0c33!important}}
.hm-note{{font-size:12px!important;margin:8px 0!important;padding:7px 10px!important}}
[data-testid="stVerticalBlockBorderWrapper"]{{border-radius:14px!important;border-color:#eee7e9!important;box-shadow:0 4px 14px #4c19300d!important}}
@media(max-width:900px){{.hm-hero{{min-height:275px!important;padding:24px!important}}.hm-hero .hm-site-name{{font-size:38px!important}}.hm-hero .hm-title{{font-size:30px!important}}}}
/* Stronger hierarchy and spacious navigation */
[data-testid="stSidebar"] .hm-brand{{font-size:42px!important;white-space:normal!important;text-align:left!important}}
[data-testid="stSidebar"] .hm-brand-small{{text-align:left!important;letter-spacing:1.7px!important}}
[data-testid="stSidebar"] .stPageLink a{{font-size:16px!important;min-height:48px!important;padding:11px 12px!important;white-space:normal!important}}
[data-testid="stSidebar"] .stPageLink a[aria-current="page"]{{background:#850b35!important;color:white!important}}
.hm-card .hm-k-num{{font-size:46px!important;text-shadow:0 1px 0 #ffffff70}}
.hm-card .hm-k-label{{font-size:17px!important}}
.hm-card .hm-k-note{{font-size:13px!important;color:#51223a!important}}
.hm-hero .hm-sub{{font-size:17px!important}}
/* KPI legibility: Unicode Vietnamese-friendly font stack + crisp white outline */
.hm-card .hm-k-num,
.hm-card .hm-k-label{{
  font-family: "Noto Serif", "DejaVu Serif", Georgia, "Times New Roman", serif!important;
  color:#80092f!important;
  -webkit-text-stroke: 0.85px #fff!important;
  paint-order:stroke fill;
  text-shadow: 1px 1px 0 #fff, -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 0 2px 5px rgba(255,255,255,.75)!important;
}}
.hm-card .hm-k-label{{font-size:17px!important;font-weight:800!important;line-height:1.35!important}}
.hm-card .hm-k-note{{
  font-family: "Arial", "DejaVu Sans", sans-serif!important;
  font-size:13px!important;font-weight:650!important;
  color:#4b1930!important;
  -webkit-text-stroke: 0.35px white!important;
  text-shadow: 0 1px 2px #fff, 1px 0 1px #fff, -1px 0 1px #fff!important;
}}

/* FINAL FIX: Vietnamese typography, prevent brand wrapping, readable KPI */
[data-testid="stSidebar"] {{ width:310px!important; min-width:310px!important; max-width:310px!important; }}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{ padding-left:20px!important; padding-right:20px!important; }}
[data-testid="stSidebar"] .hm-brand {{
 font-family:Georgia,"Times New Roman",serif!important;
 font-size:34px!important;letter-spacing:-1.7px!important;
 white-space:nowrap!important;overflow:visible!important;
 word-break:normal!important;overflow-wrap:normal!important;
 line-height:1.2!important;max-width:100%!important;
}}
.hm-card .hm-k-num {{
 font-family:Georgia,"Times New Roman",serif!important;
 font-size:clamp(35px,2.5vw,46px)!important;
 line-height:1.13!important;letter-spacing:-1px!important;
 color:#850b35!important;-webkit-text-stroke:0.45px #fff!important;
 text-shadow:1px 1px 0 #fff,-1px -1px 0 #fff,1px -1px 0 #fff,-1px 1px 0 #fff!important;
 white-space:nowrap!important;
}}
.hm-card .hm-k-label {{
 font-family:Arial,"Segoe UI",Tahoma,sans-serif!important;
 font-size:17px!important;font-weight:800!important;
 letter-spacing:0!important;word-spacing:normal!important;
 font-kerning:normal!important;line-height:1.4!important;
 color:#67112f!important;-webkit-text-stroke:0!important;
 text-shadow:1px 1px 0 #fff,-1px -1px 0 #fff,1px -1px 0 #fff,-1px 1px 0 #fff,0 0 4px #fff!important;
 white-space:normal!important;overflow-wrap:normal!important;word-break:normal!important;
}}
.hm-card .hm-k-note {{
 font-family:Arial,"Segoe UI",Tahoma,sans-serif!important;
 font-size:13px!important;font-weight:600!important;
 letter-spacing:0!important;word-spacing:normal!important;
 color:#4b1930!important;-webkit-text-stroke:0!important;
 text-shadow:0 1px 2px #fff,0 0 4px #fff!important;
}}
@media(max-width:800px){{[data-testid="stSidebar"]{{width:280px!important;min-width:280px!important;max-width:280px!important}}[data-testid="stSidebar"] .hm-brand{{font-size:30px!important}}}}

/* FINAL VISUAL PASS: high-contrast navigation + larger site typography */
html,body,[data-testid="stAppViewContainer"]{{font-family:"Segoe UI",Arial,Tahoma,sans-serif!important;font-size:18px!important}}
[data-testid="stSidebar"]{{width:340px!important;min-width:340px!important;max-width:340px!important;flex:0 0 340px!important}}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{{padding-left:22px!important;padding-right:22px!important}}
[data-testid="stSidebar"] .hm-brand{{font-family:Georgia,"Times New Roman",serif!important;font-size:clamp(30px,2.1vw,38px)!important;letter-spacing:-1.8px!important;white-space:nowrap!important;word-break:keep-all!important;overflow-wrap:normal!important;line-height:1.18!important}}
[data-testid="stSidebar"] .hm-brand-small{{font-size:12px!important;letter-spacing:1.4px!important;font-weight:700!important}}
[data-testid="stSidebar"] .hm-nav-title{{font-size:14px!important;font-weight:800!important;color:#8d4c62!important;letter-spacing:1.7px!important}}
[data-testid="stSidebar"] .stPageLink a,[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]{{font-family:"Segoe UI",Arial,Tahoma,sans-serif!important;font-size:18px!important;font-weight:800!important;color:#790b31!important;letter-spacing:0!important;min-height:54px!important;line-height:1.35!important;padding:12px 14px!important;white-space:nowrap!important;transform:none!important}}
[data-testid="stSidebar"] .stPageLink a svg,[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] svg{{color:#960e40!important;flex-shrink:0!important;width:21px!important;height:21px!important}}
[data-testid="stSidebar"] .stPageLink a:hover{{background:#f7e6ed!important;color:#640523!important}}
[data-testid="stSidebar"] .stPageLink a[aria-current="page"],[data-testid="stSidebar"] .stPageLink a[aria-current="true"],[data-testid="stSidebar"] .stPageLink:has([aria-current="page"]) a,[data-testid="stSidebar"] .stPageLink:has([aria-current="true"]) a{{background:#f5dfe8!important;color:#790b31!important;border-left:4px solid #9b1749!important;box-shadow:none!important}}
[data-testid="stSidebar"] .stPageLink a[aria-current] svg,[data-testid="stSidebar"] .stPageLink:has([aria-current]) svg{{color:#790b31!important}}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{{font-size:16px!important;font-weight:750!important;color:#6c1d3c!important}}
.hm-hero .hm-site-name{{font-size:clamp(47px,4.3vw,72px)!important}}
.hm-hero .hm-title{{font-size:clamp(35px,3.2vw,53px)!important}}
.hm-hero .hm-eyebrow{{font-size:14px!important}}
.hm-section{{font-size:30px!important}}
.hm-heading{{font-size:24px!important}}
.hm-card .hm-k-num{{font-size:clamp(43px,3vw,54px)!important}}
.hm-card .hm-k-label{{font-size:19px!important;font-weight:800!important;letter-spacing:0!important;word-spacing:normal!important;line-height:1.32!important;-webkit-text-stroke:0!important;text-shadow:0 0 3px #fff,1px 1px 0 #fff,-1px -1px 0 #fff!important}}
.hm-card .hm-k-note{{font-size:15px!important;font-weight:650!important}}
.hm-note{{font-size:15px!important;line-height:1.55!important}}
.hm-table{{font-size:17px!important}}.hm-table th{{font-size:15px!important}}
[data-testid="stMarkdownContainer"] p,[data-testid="stWidgetLabel"] p{{font-size:17px;line-height:1.55}}
[data-testid="stSelectbox"] *,[data-testid="stMultiSelect"] *,[data-testid="stTextInput"] input{{font-size:16px!important}}
[data-testid="stDataFrame"]{{font-size:16px!important}}
@media(max-width:900px){{[data-testid="stSidebar"]{{width:300px!important;min-width:300px!important;max-width:300px!important}}[data-testid="stSidebar"] .hm-brand{{font-size:32px!important}}[data-testid="stSidebar"] .stPageLink a{{font-size:16px!important}}.hm-section{{font-size:25px!important}}}}
</style>""",unsafe_allow_html=True)

@st.cache_data

def load_evidence():

    path = DATA / 'Evidence_Final.xlsx'

    if not path.exists(): raise FileNotFoundError(f'Không tìm thấy {path}')

    d = pd.read_excel(path, sheet_name='Evidence_Raw', engine='openpyxl')

    d.columns = d.columns.astype(str).str.strip()

    required = ['bank','criterion','filename','page','context']

    missing = [c for c in required if c not in d.columns]

    if missing: raise ValueError(f'Thiếu cột: {missing}')

    d['bank'] = d['bank'].astype('string').str.strip().replace({'VTB':'VietinBank','Vietinbank':'VietinBank'})

    d['criterion'] = d['criterion'].astype('string').str.strip().str.upper()

    d['pillar'] = d['criterion'].str[0]

    d['pillar_name'] = d['pillar'].map(PILLARS)

    if 'criterion_name' not in d.columns: d['criterion_name'] = d['criterion']

    if 'filter_stage' not in d.columns: d['filter_stage'] = 'Không phân loại'

    d['filter_stage'] = d['filter_stage'].astype('string').fillna('Không phân loại').str.strip()

    return d



@st.cache_data

def load_ranking():

    path = DATA / 'ranking.csv'

    if not path.exists(): return None

    d = pd.read_csv(path, encoding='utf-8-sig')

    if not {'bank','rank','BDTI','A','B','C','D'}.issubset(d.columns): return None

    for c in ['rank','BDTI','A','B','C','D']:

        d[c] = pd.to_numeric(d[c],errors='coerce')

    return d.dropna(subset=['rank','BDTI']).sort_values(['rank','bank'])



try:

    evidence = load_evidence()

    ranking = load_ranking()

except Exception as e:

    st.error(f'Lỗi tải dữ liệu: {e}')

    st.stop()



with st.sidebar:

    st.markdown('<div class="hm-brand">HerMetrics</div><div class="hm-brand-small">BANKING INTELLIGENCE</div>',unsafe_allow_html=True)


    st.markdown('<div class="hm-nav-title">WORKSPACE</div>',unsafe_allow_html=True)

    st.page_link('app.py',label='Overview',icon='📊')

    st.page_link('pages/2_Ranking_Dashboard.py',label='Ranking',icon='🏆')

    st.page_link('pages/3_Bank_Profile.py',label='Bank Profile',icon='🏦')

    st.page_link('pages/4_Bank_Comparison.py',label='Bank Comparison',icon='⚖️')

    st.page_link('pages/1_Evidence_Explorer.py',label='Evidence Explorer',icon='🔎')

    st.page_link('pages/5_Scoring_Evidence_Audit.py',label='Scoring Audit',icon='📋')

    st.page_link('pages/6_Data_Validation.py',label='Data Validation',icon='✅')

    st.markdown('<div class="hm-sidebar-art" aria-label="Phong cảnh Việt Nam"></div>',unsafe_allow_html=True)

    st.markdown('---')

    with st.container(border=True):
        st.markdown('<div class="hm-filter-heading">EVIDENCE FILTERS</div>', unsafe_allow_html=True)

        banks_present = [b for b in BANKS if b in evidence['bank'].dropna().unique()]

        selected_banks = st.multiselect('Ngân hàng', banks_present, default=banks_present)

        selected_pillars = st.multiselect('Trụ cột', list(PILLARS), default=list(PILLARS),format_func=lambda p:f'{p} — {PILLARS[p]}')

        available_criteria = [c for c in CRITERIA if c[0] in selected_pillars and c in evidence['criterion'].dropna().unique()]

        selected_criteria = st.multiselect('Tiêu chí',available_criteria,default=available_criteria)

        stages = sorted(evidence['filter_stage'].dropna().unique().tolist())

        selected_stages = st.multiselect('Tầng bằng chứng',stages,default=stages)

    st.markdown('---')

    st.caption('HerMetrics · Vietnam Banking 2025')



# Navigation override applied after sidebar widgets have been created.
# Streamlit page_link uses nested elements, so style the link AND its children.
st.markdown("""<style>
section[data-testid="stSidebar"] {
  min-width: 340px !important;
  width: 340px !important;
  max-width: 340px !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
  padding-left: 22px !important;
  padding-right: 22px !important;
}
section[data-testid="stSidebar"] .hm-brand {
  font-family: Georgia, "Times New Roman", serif !important;
  font-size: 39px !important;
  font-weight: 800 !important;
  letter-spacing: -1.5px !important;
  white-space: nowrap !important;
  overflow-wrap: normal !important;
  word-break: keep-all !important;
  color: #800c35 !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
section[data-testid="stSidebar"] .stPageLink a,
section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
  background: transparent !important;
  border-radius: 13px !important;
  padding: 13px 14px !important;
  min-height: 56px !important;
  text-decoration: none !important;
  color: #790b31 !important;
  font-family: "Segoe UI", Arial, Tahoma, sans-serif !important;
  font-size: 19px !important;
  font-weight: 800 !important;
  line-height: 1.25 !important;
  letter-spacing: 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
section[data-testid="stSidebar"] .stPageLink a p,
section[data-testid="stSidebar"] [data-testid="stPageLink"] a p {
  color: inherit !important;
  font-family: "Segoe UI", Arial, Tahoma, sans-serif !important;
  font-size: 19px !important;
  font-weight: 800 !important;
  line-height: 1.25 !important;
  letter-spacing: 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] svg,
section[data-testid="stSidebar"] .stPageLink a svg {
  color: #990e42 !important;
  fill: none !important;
  stroke: currentColor !important;
  width: 23px !important;
  height: 23px !important;
  flex-shrink: 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover,
section[data-testid="stSidebar"] .stPageLink a:hover {
  background: #f9e7ef !important;
  color: #6d082d !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="true"],
section[data-testid="stSidebar"] .stPageLink a[aria-current="page"],
section[data-testid="stSidebar"] .stPageLink a[aria-current="true"] {
  background: #f6dfe9 !important;
  color: #790b31 !important;
  border-left: 4px solid #9b1749 !important;
}
@media (max-width: 850px) {
  section[data-testid="stSidebar"] { min-width: 300px !important; width: 300px !important; max-width: 300px !important; }
  section[data-testid="stSidebar"] .hm-brand { font-size: 34px !important; }
  section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
  section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] :is(p,span) {font-size: 17px !important;}
}

/* Distinct evidence-filter panel in sidebar */
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) {
  background: linear-gradient(155deg, #fff1f6 0%, #fbe4ed 100%) !important;
  border: 1.5px solid #dca4b9 !important;
  border-radius: 18px !important;
  box-shadow: 0 5px 18px rgba(116,27,59,.09) !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) > div {
  padding: 15px 14px !important;
}
section[data-testid="stSidebar"] .hm-filter-heading {
  font: 800 17px/1.35 "Segoe UI", Arial, sans-serif !important;
  letter-spacing: 1.3px !important;
  color: #790b31 !important;
  padding: 0 0 12px !important;
  border-bottom: 1px solid #e4b5c6;
  margin-bottom: 12px;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) [data-testid="stWidgetLabel"] p {
  font: 800 16px/1.4 "Segoe UI", Arial, sans-serif !important;
  color: #741b3b !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) span[data-baseweb="tag"] {
  background: #a83460 !important;
  color: #fff !important;
  border: 1px solid #90284e !important;
  border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) span[data-baseweb="tag"] :is(span,svg) {
  color: #fff !important;
  fill: none !important;
}
</style>""", unsafe_allow_html=True)

st.markdown("<style>" + '\n/* Final reliable sidebar styles: do not alter icon glyph fonts */\nsection[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,\nsection[data-testid="stSidebar"] .stPageLink a p {\n  color: #790b31 !important;\n  font-family: "Segoe UI", Arial, sans-serif !important;\n  font-size: 19px !important;\n  font-weight: 800 !important;\n  letter-spacing: 0 !important;\n  margin: 0 !important;\n}\nsection[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {\n  display: flex !important;\n  align-items: center !important;\n  gap: 12px !important;\n}\nsection[data-testid="stSidebar"] [data-baseweb="tag"] {\n  background-color: #9a3157 !important;\n  color: #fff !important;\n  border-radius: 8px !important;\n}\nsection[data-testid="stSidebar"] [data-baseweb="tag"] span,\nsection[data-testid="stSidebar"] [data-baseweb="tag"] svg {color:#fff !important;}\n' + "</style>", unsafe_allow_html=True)


# Final targeted overrides: scoped to actual Streamlit DOM; preserve Material icon fonts.
st.markdown(r"""<style>
/* Exactly two headline lines, with responsive sizing instead of natural word wrapping */
.hm-hero .hm-title {max-width:none !important; width:100% !important; font-size:clamp(24px,2.65vw,43px) !important; line-height:1.12 !important;}
.hm-hero .hm-title-line {display:block !important; white-space:nowrap !important; letter-spacing:-.9px !important;}
@media(max-width:750px){.hm-hero .hm-title {font-size:clamp(18px,4vw,28px) !important;}}
/* Wide sidebar and readable controls */
section[data-testid="stSidebar"] {width:370px !important; min-width:370px !important; max-width:370px !important;}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {padding-left:22px !important;padding-right:22px !important;}
section[data-testid="stSidebar"] .hm-brand {font-size:39px !important;white-space:nowrap !important;}
/* Style ONLY text labels; avoid applying text fonts to Material Symbols icon glyphs */
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
section[data-testid="stSidebar"] .stPageLink a p {font-family:Arial,'Segoe UI',sans-serif !important;font-size:19px !important;font-weight:800 !important;color:#790b31 !important;line-height:1.35 !important;letter-spacing:0 !important;}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {min-height:54px !important;display:flex !important;align-items:center !important;gap:12px !important;}
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span[data-testid="stIconMaterial"],
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] .material-symbols-rounded,
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] .material-icons {font-family:'Material Symbols Rounded','Material Icons' !important;font-weight:normal !important;font-size:23px !important;letter-spacing:normal !important;white-space:nowrap !important;line-height:1 !important;color:#890c39 !important;}
/* Evidence panel */
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) {background:#fff0f5 !important;border:2px solid #dba0b6 !important;border-radius:16px !important;box-shadow:0 4px 15px #741b3b16 !important;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) [data-testid="stWidgetLabel"] p {font:800 17px/1.4 Arial,'Segoe UI',sans-serif !important;color:#741b3b !important;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) [data-baseweb="tag"] {background-color:#9a3157 !important;border-radius:7px !important;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) [data-baseweb="tag"] span {color:white !important;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.hm-filter-heading) [data-baseweb="tag"] svg {color:white !important;}
</style>""",unsafe_allow_html=True)

filtered = evidence[

    evidence['bank'].isin(selected_banks)

    & evidence['pillar'].isin(selected_pillars)

    & evidence['criterion'].isin(selected_criteria)

    & evidence['filter_stage'].isin(selected_stages)

].copy()



st.markdown('''<div class="hm-hero"><div class="hm-site-name">HerMetrics</div><div class="hm-eyebrow">VIETNAM COMMERCIAL BANKS</div>

<div class="hm-title"><span class="hm-title-line">Digital Transformation</span><span class="hm-title-line">Ranking 2025</span></div>

</div>''',unsafe_allow_html=True)



# Dashboard KPIs, all calculated from filtered evidence

kpis = [

    ('Ngân hàng',str(filtered['bank'].nunique()),'Đang hiển thị'),

    ('Tiêu chí',str(filtered['criterion'].nunique()),'Trong bộ lọc hiện tại'),

    ('Dòng bằng chứng',f'{len(filtered):,}','Số dòng dữ liệu nguồn'),

    ('Nguồn báo cáo',str(filtered['filename'].nunique()),'Tệp tài liệu được ghi nhận')

]

cols = st.columns(4,gap='small')

for i,(col,(label,num,note)) in enumerate(zip(cols,kpis),start=1):

    with col:

        st.markdown(f'<div class="hm-card kpi-{i}"><div class="hm-k-num">{escape(num)}</div><div class="hm-k-label">{escape(label)}</div><div class="hm-k-note">{escape(note)}</div></div>',unsafe_allow_html=True)



st.markdown('<div class="hm-note">Các chỉ số trên phản ánh <b>số lượng bằng chứng sau khi lọc</b>, không phải điểm BDTI. BDTI là điểm ước tính từ quy trình chấm tự động, chưa được xác nhận độc lập.</div>',unsafe_allow_html=True)




st.markdown('<div class="hm-section">Banking Intelligence Overview</div>',unsafe_allow_html=True)

left, right = st.columns([1.28,1],gap='medium')

with left:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Overall Ranking 2025</div>',unsafe_allow_html=True)

        if ranking is None:

            st.info('Chưa có ranking.csv hợp lệ để hiển thị bảng xếp hạng.')

        else:

            rank_show = ranking[ranking['bank'].isin(selected_banks)].sort_values('rank')

            if rank_show.empty: st.info('Không có ngân hàng trong bộ lọc.')

            else:

                rows = []

                for _,r in rank_show.iterrows():

                    score = float(r['BDTI'])

                    width = max(0,min(100,score))

                    rows.append(f'<tr><td><b>#{int(r["rank"])}</b></td><td>{escape(str(r["bank"]))}</td><td style="width:44%"><div style="background:#f7edf1;border-radius:6px;height:12px"><div class="hm-bar" style="width:{width:.2f}%"></div></div></td><td><b>{score:.3f}</b></td></tr>')

                st.markdown('<table class="hm-table"><thead><tr><th>Hạng</th><th>Ngân hàng</th><th>BDTI</th><th>Điểm / 100</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>',unsafe_allow_html=True)

                st.caption('Nguồn: ranking.csv · Chỉ lọc ngân hàng; điểm BDTI không tính lại theo bộ lọc bằng chứng. Kết quả chấm tự động cần rà soát.')

with right:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Performance by Dimension</div>',unsafe_allow_html=True)

        if ranking is None or ranking.empty:

            st.info('Chưa có điểm trụ cột.')

        else:

            eligible = ranking[ranking['bank'].isin(selected_banks)]['bank'].tolist()

            if eligible:

                bank = st.selectbox('Ngân hàng phân tích',eligible,key='overview_radar_bank')

                r = ranking.loc[ranking['bank'].eq(bank)].iloc[0]

                vals = [float(r[p]) for p in PILLARS]

                fig = go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=list(PILLARS)+['A'],fill='toself',fillcolor='rgba(155,56,91,.16)',line=dict(color='#741b3b',width=3),marker=dict(size=7),name=bank))

                fig.update_layout(height=325,showlegend=False,margin=dict(l=35,r=35,t=18,b=10),paper_bgcolor='rgba(0,0,0,0)',font=dict(color='#586275'),polar=dict(bgcolor='rgba(0,0,0,0)',radialaxis=dict(range=[0,100],gridcolor='#eee6eb',tickvals=[25,50,75,100]),angularaxis=dict(gridcolor='#eee6eb')))

                st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

            else: st.info('Hãy chọn ít nhất một ngân hàng.')



st.markdown('<div class="hm-section">Evidence Analytics</div>',unsafe_allow_html=True)

col_a,col_b = st.columns([1.15,1],gap='medium')

with col_a:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Evidence by Bank</div>',unsafe_allow_html=True)

        counts = filtered.groupby('bank').size().reindex(BANKS,fill_value=0)

        fig = go.Figure(go.Bar(x=counts.values,y=counts.index,orientation='h',marker_color=[BANK_COLORS[b] for b in BANKS],text=counts.values,textposition='outside'))

        fig.update_layout(height=330,showlegend=False,margin=dict(l=8,r=45,t=12,b=25),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='Số dòng bằng chứng',gridcolor='#f0edf0'),yaxis=dict(autorange='reversed',title=''))

        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

with col_b:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Evidence by Pillar</div>',unsafe_allow_html=True)

        pc = filtered.groupby('pillar').size().reindex(list(PILLARS),fill_value=0)

        fig = go.Figure(go.Bar(x=pc.index,y=pc.values,marker_color=[PILLAR_COLORS[p] for p in pc.index],text=pc.values,textposition='outside'))

        fig.update_layout(height=330,showlegend=False,margin=dict(l=10,r=10,t=12,b=25),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='Trụ cột'),yaxis=dict(title='Số dòng bằng chứng',gridcolor='#f0edf0'))

        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})



st.markdown('<div class="hm-section">Evidence Matrix</div>',unsafe_allow_html=True)

with st.container(border=True):

    st.markdown('<div class="hm-heading">5 Banks × 16 Criteria</div>',unsafe_allow_html=True)

    heat = filtered.groupby(['bank','criterion']).size().unstack(fill_value=0).reindex(index=BANKS,columns=CRITERIA,fill_value=0)

    fig = px.imshow(heat,aspect='auto',text_auto=True,color_continuous_scale=['#fff6f9','#e8afc2','#a8496b','#641b38'],labels={'x':'Tiêu chí','y':'Ngân hàng','color':'Số dòng'})

    fig.update_layout(height=380,margin=dict(l=5,r=5,t=12,b=20),paper_bgcolor='rgba(0,0,0,0)',font=dict(color='#364055'))

    st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

    st.caption('Số dòng bằng chứng không phản ánh trực tiếp mức độ chuyển đổi số hoặc điểm BDTI.')



st.markdown('<div class="hm-section">Evidence Explorer</div>',unsafe_allow_html=True)

with st.container(border=True):

    keyword = st.text_input('Tìm kiếm nội dung hoặc tên báo cáo',placeholder='Nhập từ khóa...')

    shown = filtered.copy()

    if keyword.strip():

        text = shown['context'].fillna('').astype(str)+' '+shown['filename'].fillna('').astype(str)+' '+shown['criterion_name'].fillna('').astype(str)

        shown = shown[text.str.contains(keyword.strip(),case=False,regex=False,na=False)]

    st.caption(f'Tìm thấy {len(shown):,} dòng bằng chứng')

    cols = ['bank','pillar','criterion','criterion_name','filter_stage','filename','page','context']

    st.dataframe(shown[cols],width='stretch',height=390,hide_index=True,column_config={'bank':'Ngân hàng','pillar':'Trụ cột','criterion':'Tiêu chí','criterion_name':'Tên tiêu chí','filter_stage':'Tầng lọc','filename':'Nguồn báo cáo','page':'Trang','context':st.column_config.TextColumn('Nội dung bằng chứng',width='large')})



st.caption('HerMetrics · Banking Intelligence 2025 | Evidence_Final.xlsx & ranking.csv')
