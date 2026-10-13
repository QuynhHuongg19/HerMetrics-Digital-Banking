"""HerMetrics | Evidence Explorer — isolated Streamlit page, using real Evidence_Final.xlsx."""

from __future__ import annotations



import base64

from html import escape

from pathlib import Path



import pandas as pd

import streamlit as st



st.set_page_config(page_title="Evidence Explorer | HerMetrics", page_icon="🔎", layout="wide", initial_sidebar_state="expanded")

# HERMETRICS_SIDEBAR_V2
from pathlib import Path as _HMPath
from hermetrics_sidebar import render as _hm_render
_hm_render(_HMPath(__file__).resolve().parent.parent, show_nav=False)


ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "data" / "Evidence_Final.xlsx"

# CHỈ CẦN ĐỔI TÊN ẢNH Ở DÒNG DƯỚI (ví dụ: ha_long_cua_tui.png).

# Lưu ảnh vào assets/vietnam_art/ của đúng dự án chứa app.py.

ART_FILENAME = "vinh_ha_long_tranh_son_dau.png"

ART_PATH = ROOT / "assets" / "vietnam_art" / ART_FILENAME

DEMO_BANNER_PATH = ROOT / "assets" / "vietnam_art" / "evidence_banner_demo.png"

# Nếu chưa có tên tùy đặt, dùng chính ảnh gốc đã có trong thư mục đúng.

if not ART_PATH.is_file():

    ART_PATH = ROOT / "assets" / "vietnam_art" / "vinh_ha_long_tranh_son_dau.png"



@st.cache_data(show_spinner=False)

def load_art_image(path: str, modified: float) -> str:

    """Đưa ảnh local vào CSS/HTML dưới dạng data URI, không cần URL máy chủ."""

    import mimetypes

    mime = mimetypes.guess_type(path)[0] or "image/png"

    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")

    return f"data:{mime};base64,{encoded}"



if ART_PATH.is_file():

    ART_IMAGE = load_art_image(str(ART_PATH), ART_PATH.stat().st_mtime)

else:

    ART_IMAGE = ""

    st.warning(f"Chưa tìm thấy ảnh: {ART_PATH}. Hãy sửa ART_FILENAME đúng tên ảnh bạn đã lưu.")



PILLARS = {"A": "Chiến lược & nguồn lực số", "B": "Sản phẩm số & trải nghiệm khách hàng", "C": "Công nghệ & dữ liệu", "D": "Vận hành số & an toàn"}

BANK_ORDER = ["BIDV", "MB", "OCB", "VCB", "VietinBank"]



@st.cache_data(show_spinner=False)

def read_evidence(path: str, mtime: float) -> pd.DataFrame:

    df = pd.read_excel(path, sheet_name="Evidence_Raw", engine="openpyxl")

    df.columns = df.columns.astype(str).str.strip()

    required = ["bank", "criterion", "filename", "page", "context"]

    missing = [col for col in required if col not in df.columns]

    if missing:

        raise ValueError("Thiếu cột trong Evidence_Raw: " + ", ".join(missing))

    df["bank"] = df["bank"].astype("string").str.strip().replace({"VTB": "VietinBank", "Vietinbank": "VietinBank"})

    df["criterion"] = df["criterion"].astype("string").str.strip().str.upper()

    df["pillar"] = df["criterion"].str[0]

    df["criterion_name"] = df.get("criterion_name", df["criterion"]).astype("string").fillna("")

    df["filter_stage"] = df.get("filter_stage", pd.Series("Không phân loại", index=df.index)).astype("string").fillna("Không phân loại")

    for col in ["filename", "context"]:

        df[col] = df[col].astype("string").fillna("")

    return df.reset_index(drop=True)



if not SOURCE.exists():

    st.error(f"Không tìm thấy dữ liệu: {SOURCE}. Hãy giữ nguyên thư mục data của dự án.")

    st.stop()

try:

    data = read_evidence(str(SOURCE), SOURCE.stat().st_mtime)

except Exception as exc:

    st.error(f"Không thể đọc dữ liệu bằng chứng: {exc}")

    st.stop()



img = ART_IMAGE



css = r"""

<style>

:root{--wine:#760b32;--navy:#1c394b;--teal:#b9d6d2;--cream:#fff9ed;--sand:#f4e2b2;--line:#dce7e3}

.stApp{background:#fff;color:#213747;font-family:'Segoe UI',Arial,sans-serif}

.hm-section,.hm-hero h1,.hm-detail-value,.hm-kpi-value,.hm-brand{font-family:'Segoe UI',Arial,sans-serif!important;font-kerning:normal;letter-spacing:normal!important;word-spacing:normal!important;font-variant-ligatures:normal}

.hm-section{font-weight:800!important}

.hm-detail-value{font-weight:800!important}

.hm-hero h1{font-weight:800!important}

.hm-brand{font-weight:800!important}

.block-container{max-width:1700px;padding:1rem 1.65rem 3rem}

[data-testid="stSidebar"]{background:#fafaf6;border-right:1px solid #d8e5df;min-width:325px!important;max-width:325px!important}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding-top:1rem}

[data-testid="stSidebarNav"]{display:none!important}

.hm-brand{font:700 42px/1.05 'Segoe UI',Arial,sans-serif;color:var(--wine);white-space:nowrap;letter-spacing:-1px}

.hm-tag{font:700 12px/1.5 'Segoe UI',Arial,sans-serif;letter-spacing:1.6px;color:var(--wine);margin:8px 0 25px}

.hm-label{font:800 14px/1.5 'Segoe UI',Arial,sans-serif;color:#795764;letter-spacing:1.4px;margin:10px 0}

[data-testid="stSidebar"] .stPageLink a{border-radius:12px;padding:9px 12px!important;margin-bottom:2px}

[data-testid="stSidebar"] .stPageLink a p{font-family:'Segoe UI',Arial,sans-serif!important;font-weight:800!important;font-size:17px!important;color:var(--wine)!important;letter-spacing:0!important}

[data-testid="stSidebar"] .stPageLink a:hover{background:#e4efec}

[data-testid="stSidebar"] .stPageLink a[aria-current="page"]{background:#d9e9e4!important}

[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]{background:transparent}

[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]{border-color:#a9cbc3!important;border-radius:16px!important;background:linear-gradient(155deg,#eff7f4,#fffaf1)!important}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-weight:750!important;color:var(--wine)!important;font-size:15px!important}

[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#e8f2ef!important;border-color:#c5dad4!important;border-radius:9px!important}

[data-testid="stSidebar"] [data-baseweb="tag"]{background:#327b78!important}

 .hm-side-art{margin-top:14px;border-radius:15px;overflow:hidden;border:1px solid #b6d1c9;box-shadow:0 6px 16px rgba(26,73,70,.10)}

.hm-side-art img{width:100%;height:auto;aspect-ratio:1.6;object-fit:cover;object-position:center;display:block}

.hm-filter{font:800 18px/1.4 "Segoe UI",Arial,sans-serif;color:var(--wine);letter-spacing:.6px;border-bottom:1px solid #bbd4cd;padding-bottom:10px;margin-bottom:7px}

.hm-hero{height:248px;position:relative;overflow:hidden;border-radius:18px;border:1px solid #b5d3ca;background:#f9f8f1;padding:34px 35px;margin:0 0 12px}

.hm-hero-art{position:absolute;right:0;top:0;width:100%;height:100%;object-fit:cover;object-position:center 57%;display:block;z-index:0}

.hm-hero:before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,rgba(250,249,242,.99) 0%,rgba(250,249,242,.97) 22%,rgba(250,249,242,.84) 39%,rgba(250,249,242,.25) 62%,rgba(250,249,242,0) 83%)}

.hm-hero-content{position:relative;z-index:2}

.hm-eyebrow{font:700 15px 'Segoe UI',Arial,sans-serif;letter-spacing:3px;color:var(--wine)}

.hm-hero h1{font:800 clamp(35px,3.4vw,55px)/1.14 'Segoe UI',Arial,sans-serif!important;color:var(--wine)!important;margin:9px 0!important;letter-spacing:normal}

.hm-hero p{font:500 17px 'Segoe UI',Arial,sans-serif;color:var(--navy)}

.hm-kpi{border:1px solid #d8e6e0;border-radius:17px;padding:18px 18px;min-height:125px;background:#e8f3f1;display:flex;align-items:center;gap:16px}

.hm-kpi.k1{background:linear-gradient(125deg,#f2d5c6,#fae7dd)}

.hm-kpi.k2{background:linear-gradient(125deg,#b7dfd9,#e2f3ee)}

.hm-kpi.k3{background:linear-gradient(125deg,#f9df9e,#fff1cc)}

.hm-kpi.k4{background:linear-gradient(125deg,#cbdcbb,#edf3df)}

.hm-kpi-icon{display:flex;align-items:center;justify-content:center;flex:0 0 54px;height:54px;border-radius:15px;background:rgba(255,255,255,.38);font-size:30px;color:var(--wine)}

.hm-kpi-label{font:750 17px 'Segoe UI',Arial,sans-serif;color:#274253}

.hm-kpi-value{font:800 45px/1.2 'Segoe UI',Arial,sans-serif;color:var(--wine)}

.hm-section{font:800 32px/1.3 'Segoe UI',Arial,sans-serif;color:var(--wine);border-left:5px solid var(--wine);padding-left:16px;margin:16px 0 6px}

.hm-help{font:15px 'Segoe UI',Arial,sans-serif;color:#61717d;margin:0 0 10px 20px}

.hm-details{border:1px solid #d8e6e0;border-radius:14px;background:#fff;border:1px solid #c5ddd5;padding:16px 20px;margin:8px 0 10px}

.hm-detail-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}

.hm-detail-cell{background:linear-gradient(115deg,#e4f2ef,#fff6dc);border:1px solid #c4dcd5;border-radius:10px;padding:12px 14px;min-width:0}

.hm-detail-label{font:600 13px 'Segoe UI',Arial,sans-serif;color:#516d70}

.hm-detail-value{font:800 24px 'Segoe UI',Arial,sans-serif;color:var(--wine);overflow-wrap:anywhere}

.hm-quote{font:18px/1.75 'Segoe UI',Arial,sans-serif;color:#173c45;background:linear-gradient(115deg,#e6f4f0,#fff3d2);border-left:5px solid #267a78;border-radius:9px;padding:17px 19px;white-space:pre-wrap;overflow-wrap:anywhere;margin:12px 0}

.hm-meta{font:16px/1.65 'Segoe UI',Arial,sans-serif;color:#30495a;margin:12px 0}

[data-testid="stTextInput"] input{font-size:17px!important}





[data-testid="stMarkdownContainer"] p{line-height:1.55}

@media(max-width:900px){.hm-hero{height:210px;padding:22px}.hm-hero-art{height:100%}.hm-detail-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hm-hero h1{font-size:38px!important}}

.hm-demo-banner{width:100%;margin:0 0 12px;line-height:0}

.hm-demo-banner img{width:100%;height:auto;display:block;border-radius:17px}


/* Bảng bằng chứng HTML: màu header được áp dụng trực tiếp, không phụ thuộc st.dataframe */
.hm-table-scroll{max-height:460px;overflow:auto;border:1px solid #9bc7bf;border-radius:13px;box-shadow:0 5px 20px rgba(19,92,86,.07)}
.hm-evidence-table{width:100%;min-width:1140px;border-collapse:separate;border-spacing:0;font-family:'Segoe UI',Arial,sans-serif;font-size:15px;color:#213747}
.hm-evidence-table thead th{position:sticky;top:0;z-index:2;background:#176b68!important;color:#fff!important;text-align:left;font-size:15px;font-weight:800;padding:14px 12px;white-space:nowrap;border-right:1px solid rgba(255,255,255,.2)}
.hm-evidence-table tbody td{padding:11px 12px;border-bottom:1px solid #dce9e5;vertical-align:top;max-width:480px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hm-evidence-table tbody tr:nth-child(odd){background:#fff}
.hm-evidence-table tbody tr:nth-child(even){background:#eef8f5}
.hm-evidence-table tbody tr.hm-selected{background:#d2eee7!important;box-shadow:inset 4px 0 #176b68}
.hm-evidence-table tbody td.hm-key{color:#760b32;font-weight:800}
.hm-evidence-table tbody tr:hover{background:#dff3ed}
</style>

"""



st.markdown(css, unsafe_allow_html=True)



with st.sidebar:

    st.markdown('<div class="hm-brand">HerMetrics</div><div class="hm-tag">BANKING INTELLIGENCE</div><div class="hm-label">WORKSPACE</div>', unsafe_allow_html=True)

    links = [

        ("app.py", "Overview", "📊"),

        ("pages/2_Ranking_Dashboard.py", "Ranking", "📈"),

        ("pages/3_Bank_Profile.py", "Bank Profile", "🏦"),

        ("pages/4_Bank_Comparison.py", "Bank Comparison", "⚖️"),

        ("pages/1_Evidence_Explorer.py", "Evidence Explorer", "🔎"),

        ("pages/5_Scoring_Evidence_Audit.py", "Scoring Audit", "📋"),

        ("pages/6_Data_Validation.py", "Data Validation", "✅"),

    ]

    for path, title, icon in links:

        if (ROOT / path).exists():

            st.page_link(path, label=title, icon=icon)

    st.markdown(" ")

    with st.container(border=True):

        st.markdown('<div class="hm-filter">EVIDENCE FILTERS</div>', unsafe_allow_html=True)

        banks = [b for b in BANK_ORDER if b in data["bank"].dropna().unique()]

        banks += sorted(set(data["bank"].dropna().tolist()) - set(banks))

        bank = st.selectbox("Ngân hàng", ["Tất cả"] + banks, key="ev_bank")

        pillar_options = [p for p in PILLARS if p in data["pillar"].dropna().unique()]

        pillar = st.selectbox("Trụ cột", ["Tất cả"] + pillar_options, format_func=lambda p: "Tất cả" if p == "Tất cả" else f"{p} — {PILLARS[p]}", key="ev_pillar")

        criteria_pool = data if pillar == "Tất cả" else data[data["pillar"] == pillar]

        criteria = sorted(criteria_pool["criterion"].dropna().unique().tolist())

        criterion = st.selectbox("Tiêu chí", ["Tất cả"] + criteria, key="ev_criterion")

        stages = sorted(data["filter_stage"].dropna().unique().tolist())

        stage = st.selectbox("Tầng bằng chứng", ["Tất cả"] + stages, key="ev_stage")

    if ART_IMAGE:

        st.markdown(

        f'<div class="hm-side-art"><img src="{ART_IMAGE}" alt="Tranh gốc Vịnh Hạ Long với thuyền buồm và núi đá"></div>',

        unsafe_allow_html=True,

    )





if DEMO_BANNER_PATH.is_file():

    demo_uri = load_art_image(str(DEMO_BANNER_PATH), DEMO_BANNER_PATH.stat().st_mtime)

    st.markdown(

        f'<div class="hm-demo-banner"><img src="{demo_uri}" alt="Evidence Explorer - Vịnh Hạ Long" /></div>',

        unsafe_allow_html=True,

    )

else:

    st.error(f"Không tìm thấy ảnh banner mẫu: {DEMO_BANNER_PATH}. Hãy chép ảnh trong ZIP vào đúng thư mục.")



search = st.text_input("Tìm kiếm bằng chứng", placeholder="Nhập từ khóa nội dung hoặc tên báo cáo…", label_visibility="collapsed")

filtered = data.copy()

if bank != "Tất cả": filtered = filtered[filtered["bank"] == bank]

if pillar != "Tất cả": filtered = filtered[filtered["pillar"] == pillar]

if criterion != "Tất cả": filtered = filtered[filtered["criterion"] == criterion]

if stage != "Tất cả": filtered = filtered[filtered["filter_stage"] == stage]

if search.strip():

    term = search.strip()

    cols = ["context", "filename", "criterion_name", "bank", "criterion", "matched_keyword"]

    mask = pd.Series(False, index=filtered.index)

    for col in cols:

        if col in filtered.columns:

            mask |= filtered[col].astype("string").str.contains(term, case=False, regex=False, na=False)

    filtered = filtered[mask]



kpis = [("Dòng bằng chứng", f"{len(filtered):,}", "k1", "▤"), ("Ngân hàng", str(filtered["bank"].nunique()), "k2", "▥"), ("Tiêu chí", str(filtered["criterion"].nunique()), "k3", "☷"), ("Tầng bằng chứng", str(filtered["filter_stage"].nunique()), "k4", "▱")]

cols = st.columns(4, gap="medium")

for col, (label, val, cls, icon) in zip(cols, kpis):

    with col:

        st.markdown(f'<div class="hm-kpi {cls}"><div class="hm-kpi-icon">{escape(icon)}</div><div><div class="hm-kpi-label">{escape(label)}</div><div class="hm-kpi-value">{escape(val)}</div></div></div>', unsafe_allow_html=True)



st.markdown('<div class="hm-section">Danh sách bằng chứng</div><div class="hm-help">Chọn một dòng trong bảng để xem nội dung chi tiết. Bảng sử dụng dữ liệu thật từ Evidence_Final.xlsx.</div>', unsafe_allow_html=True)

if filtered.empty:

    st.info("Không có bằng chứng phù hợp với bộ lọc hoặc từ khóa hiện tại.")

else:

    page_size = 12

    total_pages = max(1, (len(filtered) + page_size - 1) // page_size)

    if st.session_state.get("ev_page", 1) > total_pages:

        st.session_state["ev_page"] = total_pages

    control1, control2, control3 = st.columns([6, 2, 2])

    with control2:

        st.caption(f"{len(filtered):,} dòng phù hợp")

    with control3:

        page = st.number_input("Trang", min_value=1, max_value=total_pages, value=min(st.session_state.get("ev_page", 1), total_pages), step=1, key="ev_page")

    start = (page - 1) * page_size

    shown = filtered.iloc[start:start + page_size].copy()

    display = pd.DataFrame({

        "Ngân hàng": shown["bank"].fillna("").astype(str),

        "Tiêu chí": shown["criterion"].fillna("").astype(str),

        "Tên tiêu chí": shown["criterion_name"].fillna("").astype(str),

        "Tầng bằng chứng": shown["filter_stage"].fillna("").astype(str),

        "Nguồn báo cáo": shown["filename"].fillna("").astype(str),

        "Trang": shown["page"].fillna("").astype(str),

        "Nội dung bằng chứng": shown["context"].fillna("").astype(str),

    }, index=shown.index)

    # Bảng HTML giúp tô màu header ổn định, không phụ thuộc cấu trúc st.dataframe.
    # Chọn dòng qua hộp chọn phía trên; bảng vẫn có cuộn và phân trang.
    row_options = list(range(len(shown)))
    selected_pos = st.selectbox(
        "Chọn dòng để xem chi tiết",
        options=row_options,
        format_func=lambda i: (
            f"Dòng {start + i + 1} · {shown.iloc[i]['bank']} · "
            f"{shown.iloc[i]['criterion']} · Trang {shown.iloc[i]['page']}"
        ),
        key=f"ev_selected_row_page_{page}",
    )
    chosen = shown.iloc[selected_pos]

    headings = list(display.columns)
    head_html = "".join(f"<th>{escape(str(h))}</th>" for h in headings)
    body_rows = []
    for pos, (_, record) in enumerate(display.iterrows()):
        cells = []
        for col in headings:
            value = record[col]
            safe = escape("" if pd.isna(value) else str(value))
            class_name = ' class="hm-key"' if col in ("Ngân hàng", "Tiêu chí") else ""
            cells.append(f"<td{class_name} title=\"{safe}\">{safe}</td>")
        selected_class = ' class="hm-selected"' if pos == selected_pos else ""
        body_rows.append(f"<tr{selected_class}>{''.join(cells)}</tr>")
    table_html = (
        '<div class="hm-table-scroll"><table class="hm-evidence-table">'
        f'<thead><tr>{head_html}</tr></thead>'
        f'<tbody>{"".join(body_rows)}</tbody></table></div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.caption(f"Trang {page}/{total_pages}. Chọn một dòng để cập nhật chi tiết bên dưới.")

    st.markdown('<div class="hm-section">Chi tiết bằng chứng</div>', unsafe_allow_html=True)

    def clean(v):

        return "—" if pd.isna(v) or str(v).strip() == "" else str(v)

    cells = [("Ngân hàng", clean(chosen["bank"])), ("Tiêu chí", clean(chosen["criterion"])), ("Tầng bằng chứng", clean(chosen["filter_stage"])), ("Trang báo cáo", clean(chosen["page"]))]

    card = "".join(f'<div class="hm-detail-cell"><div class="hm-detail-label">{escape(k)}</div><div class="hm-detail-value">{escape(v)}</div></div>' for k, v in cells)

    st.markdown(f'<div class="hm-details"><div class="hm-detail-grid">{card}</div><div class="hm-meta"><b>Tên tiêu chí:</b> {escape(clean(chosen["criterion_name"]))}<br><b>Nguồn báo cáo:</b> {escape(clean(chosen["filename"]))}</div><div class="hm-quote">{escape(clean(chosen["context"]))}</div></div>', unsafe_allow_html=True)

    st.caption("Dữ liệu bằng chứng phục vụ truy xuất nguồn; không đại diện cho điểm BDTI đã được xác nhận độc lập.")
