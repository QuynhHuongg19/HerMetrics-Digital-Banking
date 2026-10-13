import base64
import html
import re
import unicodedata
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.theme import apply_theme
from hermetrics_sidebar import render as render_sidebar

st.set_page_config(page_title="Scoring Evidence Audit | HerMetrics", page_icon="🔎", layout="wide")
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ART_DIR = ROOT / "assets" / "vietnam_art"
render_sidebar(ROOT, show_nav=True)
apply_theme()


def art_uri(filename):
    path = ART_DIR / filename
    if not path.is_file():
        return ""
    mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


hero_uri = art_uri("scoring_audit_hero.jpg")
sidebar_path = ART_DIR / "scoring_audit_sidebar.png"
if sidebar_path.is_file():
    with st.sidebar:
        st.image(str(sidebar_path), use_container_width=True)

st.markdown("""
<style>
.stApp {background:#ffffff !important;}
[data-testid="stSidebar"] {background:#fffaf1 !important;}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] {display:none !important;}
.block-container {padding-top:1.1rem;max-width:1500px;}
h1,h2,h3 {color:#075471 !important;}
/* Vietnamese-friendly typography throughout Scoring Audit */
[data-testid="stMain"] {font-family:"Segoe UI",Arial,sans-serif !important;}
[data-testid="stMain"] h1, [data-testid="stMain"] h2,
[data-testid="stMain"] h3, [data-testid="stMain"] p,
[data-testid="stMain"] label, [data-testid="stMain"] button,
[data-testid="stMain"] input, [data-testid="stMain"] textarea,
.hm-audit-hero, .hm-audit-heading, .hm-audit-card,
.hm-audit-kpi, .hm-audit-table {
  font-family:"Segoe UI",Arial,sans-serif !important;
  letter-spacing:normal;
  font-kerning:normal;
  font-variant-ligatures:normal;
  word-spacing:normal;
}
.hm-audit-heading, .hm-audit-card h3, .hm-audit-title {
  font-weight:750;
  line-height:1.35;
  letter-spacing:0 !important;
}

.hm-audit-hero {min-height:205px;border-radius:20px;border:1px solid #d7e8dc;padding:28px 30px;display:flex;align-items:center;background-repeat:no-repeat;background-position:center;background-size:cover;box-shadow:0 8px 25px #193b4b12;margin-bottom:14px;}
.hm-audit-kicker {font-size:11px;letter-spacing:2px;font-weight:800;color:#9c1748;}
.hm-audit-title {font-family:"Segoe UI",Arial,sans-serif;font-size:clamp(27px,3vw,42px);font-weight:800;color:#99153e;line-height:1.2;margin:8px 0;}
.hm-audit-sub {font-size:14px;color:#21495e;max-width:580px;font-weight:600;}
.hm-audit-notice {background:#fff0c9;border:1px solid #f1c964;color:#865109;border-radius:12px;padding:14px 17px;margin:12px 0 18px;font-weight:600;}
.hm-audit-heading {font-family:"Segoe UI",Arial,sans-serif;color:#075471;font-size:23px;font-weight:800;margin:18px 0 12px;}
.hm-audit-kpi {border:1.5px solid var(--bd);background:linear-gradient(120deg,var(--bg),#fff);border-radius:16px;padding:19px 20px;min-height:130px;box-shadow:0 5px 15px #294c5a12;position:relative;overflow:hidden;}
.hm-audit-kpi:after {content:"";position:absolute;right:-28px;bottom:-45px;width:130px;height:130px;border:17px solid var(--bd);border-radius:50%;opacity:.27;}
.hm-audit-kpi .label {font-size:14px;font-weight:750;color:var(--fg);}
.hm-audit-kpi .number {font-family:"Segoe UI",Arial,sans-serif;font-size:43px;line-height:1.2;font-weight:800;color:var(--fg);margin-top:10px;}
.hm-audit-kpi.pink {--bg:#ffe1e9;--bd:#f28eab;--fg:#9e1648;}
.hm-audit-kpi.blue {--bg:#d7edff;--bd:#79bafa;--fg:#095a9c;}
.hm-audit-kpi.green {--bg:#d7f4e5;--bd:#79d6a5;--fg:#08694c;}
.hm-audit-kpi.yellow {--bg:#fff0c8;--bd:#f3cb6a;--fg:#80550d;}
.hm-audit-card {padding:18px 20px;border-radius:17px;border:1.5px solid var(--bd);background:linear-gradient(145deg,var(--bg),#fff 85%);margin:8px 0 15px;box-shadow:0 4px 16px #163d4a0b;}
.hm-audit-card.pink {--bg:#ffedf1;--bd:#f1a1b7;}
.hm-audit-card.blue {--bg:#e7f4ff;--bd:#90c8f7;}
.hm-audit-card.green {--bg:#e7f9ef;--bd:#91dcb1;}
.hm-audit-card.yellow {--bg:#fff5da;--bd:#f4cd76;}
.hm-audit-card h3 {font-family:"Segoe UI",Arial,sans-serif;font-size:21px;margin:0 0 10px;color:#075471!important;}
.hm-audit-card p {margin:6px 0;color:#183c50;line-height:1.6;}
.hm-audit-table {overflow:auto;border:1px solid #badde9;border-radius:12px;margin:8px 0 15px;max-height:390px;}
.hm-audit-table table {border-collapse:collapse;width:100%;font-size:13px;background:white;}
.hm-audit-table th {background:#bfe9f1;color:#07506a;text-align:left;padding:11px;white-space:nowrap;position:sticky;top:0;}
.hm-audit-table td {padding:9px 11px;border-bottom:1px solid #e3eef2;color:#204254;}
.hm-audit-table tr:nth-child(even) td {background:#f3faff;}
[data-testid="stSelectbox"] label p {font-weight:750!important;color:#075471!important;}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {background:#f1f8ff!important;border-color:#9fcce7!important;}
[data-testid="stTextArea"] textarea {background:#f2f8ff!important;color:#153d58!important;}

/* Bright white canvas and high-contrast, elevated selector cards */
[data-testid="stMain"] {background:#fff !important;}
.st-key-audit_bank_selector, .st-key-audit_criterion_selector {
  position:relative;min-height:0;border-radius:19px;padding:16px 20px 20px;
  box-shadow:0 9px 22px rgba(30,71,99,.12);border:2px solid;
  transition:box-shadow .2s ease,transform .2s ease;
}
.st-key-audit_bank_selector {background:linear-gradient(125deg,#ffe5ef 0%,#fff5f9 74%,#ffd8e8 100%);border-color:#ef8eb3;}
.st-key-audit_criterion_selector {background:linear-gradient(125deg,#d8eeff 0%,#f2faff 74%,#cde9ff 100%);border-color:#79baf1;}
.st-key-audit_bank_selector:hover, .st-key-audit_criterion_selector:hover {box-shadow:0 13px 26px rgba(30,71,99,.18);transform:translateY(-2px);}
.st-key-audit_bank_selector [data-testid="stSelectbox"] label p {font-size:17px!important;color:#a71350!important;font-weight:800!important;}
.st-key-audit_criterion_selector [data-testid="stSelectbox"] label p {font-size:17px!important;color:#095b9d!important;font-weight:800!important;}
.st-key-audit_bank_selector [data-baseweb="select"] > div {background:#fffafd!important;border:2px solid #f1a5c4!important;border-radius:12px!important;min-height:54px!important;box-shadow:0 3px 9px #ae32621b!important;}
.st-key-audit_criterion_selector [data-baseweb="select"] > div {background:#fafdff!important;border:2px solid #a2d5ff!important;border-radius:12px!important;min-height:54px!important;box-shadow:0 3px 9px #1369a41a!important;}
.st-key-audit_bank_selector [data-baseweb="select"] span, .st-key-audit_criterion_selector [data-baseweb="select"] span {font-size:17px!important;font-weight:750!important;color:#153c57!important;}
/* Icons and controls use actual Streamlit columns, not absolute positioning. */
.hm-bank-logo,.hm-criterion-icon {
  display:flex;align-items:center;justify-content:center;
  width:76px;height:76px;max-width:100%;margin:0 auto;
  border-radius:50%;overflow:hidden;box-sizing:border-box;
}
.hm-bank-logo {background:#fff;border:2px solid #f3b6d0;box-shadow:0 4px 12px #b8215b20;}
.hm-bank-logo img {width:90%;height:90%;object-fit:contain;}
.hm-bank-monogram {color:#08665e;font-size:16px;font-weight:850;letter-spacing:0;}
.hm-criterion-icon {background:#fff;border:2px solid #a6d9fa;font-size:37px;box-shadow:0 4px 12px #1369a420;}
.st-key-audit_bank_selector [data-testid="stHorizontalBlock"],
.st-key-audit_criterion_selector [data-testid="stHorizontalBlock"] {align-items:center;}
.st-key-audit_bank_selector [data-testid="stSelectbox"],
.st-key-audit_criterion_selector [data-testid="stSelectbox"] {width:100%;}
.st-key-audit_bank_selector, .st-key-audit_criterion_selector {min-height:160px;}
@media(max-width:760px) {
  .st-key-audit_bank_selector,.st-key-audit_criterion_selector {padding:14px 12px;min-height:140px;}
  .hm-bank-logo,.hm-criterion-icon {width:54px;height:54px;}
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_data():
    scores = pd.read_csv(DATA_DIR / "processed_scores.csv", encoding="utf-8-sig")
    evidence = pd.read_csv(DATA_DIR / "selected_evidence.csv", encoding="utf-8-sig")
    for filename, df, required in [
        ("processed_scores.csv", scores, ["bank", "criterion", "criterion_name", "final_score", "reason", "rubric"]),
        ("selected_evidence.csv", evidence, ["bank", "criterion", "filename", "page", "context"]),
    ]:
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"{filename} thiếu cột: {missing}")
        for col in ("bank", "criterion"):
            df[col] = df[col].astype("string").str.strip()
    for frame in (scores, evidence):
        for col in frame.select_dtypes(include=["object", "string"]).columns:
            frame[col] = frame[col].map(
                lambda v: unicodedata.normalize("NFC", v) if isinstance(v, str) else v
            )
    scores["final_score"] = pd.to_numeric(scores["final_score"], errors="coerce")
    return scores, evidence


def safe(value):
    return html.escape(unicodedata.normalize("NFC", str(value))) if pd.notna(value) else "—"


def heading(text):
    st.markdown(f'<div class="hm-audit-heading">{html.escape(unicodedata.normalize("NFC", text))}</div>', unsafe_allow_html=True)


def card(title, body, color="blue"):
    st.markdown(f'<div class="hm-audit-card {color}"><h3>{html.escape(unicodedata.normalize("NFC", title))}</h3>{body}</div>', unsafe_allow_html=True)


def kpi(label, value, color):
    st.markdown(f'<div class="hm-audit-kpi {color}"><div class="label">{html.escape(unicodedata.normalize("NFC", label))}</div><div class="number">{html.escape(unicodedata.normalize("NFC", str(value)))}</div></div>', unsafe_allow_html=True)


def table(df):
    shown = df.astype(object).where(pd.notna(df), "—")
    st.markdown('<div class="hm-audit-table">' + shown.to_html(index=False, escape=True, border=0) + '</div>', unsafe_allow_html=True)


try:
    scores, evidence = load_data()
except Exception as exc:
    st.error(f"Không đọc được dữ liệu Scoring Audit: {exc}")
    st.stop()

background = (
    f"linear-gradient(90deg,rgba(255,253,248,.97) 0%,rgba(255,253,248,.83) 32%,rgba(255,253,248,.03) 72%),url('{hero_uri}')"
    if hero_uri else "linear-gradient(110deg,#fff8ee,#cce9fa,#e1f3e5)"
)
st.markdown(f'''<div class="hm-audit-hero" style="background-image:{background}">
<div><div class="hm-audit-kicker">HERMETRICS · BANKING INTELLIGENCE</div>
<div class="hm-audit-title">🔎 SCORING EVIDENCE AUDIT</div>
<div class="hm-audit-sub">Đối chiếu điểm chấm chuyển đổi số với bằng chứng từ báo cáo ngân hàng</div>
</div></div>''', unsafe_allow_html=True)

# Selectors: actual Streamlit widgets inside pastel cards, not static mockups.
def bank_logo(bank_name):
    """Use a real local logo when provided; otherwise display a clear text monogram."""
    slug = re.sub(r"[^a-z0-9]", "", str(bank_name).lower())
    folders = [ROOT / "assets" / "bank_logos", ROOT / "assets" / "logos", ART_DIR]
    for folder in folders:
        for extension in ("png", "jpg", "jpeg", "webp"):
            for filename in (f"{slug}.{extension}", f"{bank_name}.{extension}", f"logo_{slug}.{extension}"):
                path = folder / filename
                if path.is_file():
                    return art_uri_path(path)
    return ""


def art_uri_path(path):
    mime = "image/png" if path.suffix.lower() == ".png" else ("image/webp" if path.suffix.lower() == ".webp" else "image/jpeg")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


banks = sorted(scores["bank"].dropna().unique().tolist())
if not banks:
    st.warning("Chưa có ngân hàng trong dữ liệu.")
    st.stop()

col_bank, col_criterion = st.columns(2, gap="medium")
with col_bank:
    with st.container(key="audit_bank_selector"):
        logo_col, select_col = st.columns([1, 4], gap="small", vertical_alignment="center")
        with select_col:
            bank = st.selectbox("🏦 Chọn ngân hàng", banks, key="audit_bank")
        with logo_col:
            logo = bank_logo(bank)
            if logo:
                st.markdown(f'<div class="hm-bank-logo"><img src="{logo}" alt="Logo {safe(bank)}"></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hm-bank-logo hm-bank-monogram" title="Chưa có file logo ngân hàng">{safe(bank)}</div>', unsafe_allow_html=True)

bank_scores = scores[scores["bank"] == bank].copy()
criteria = sorted(bank_scores["criterion"].dropna().unique().tolist(), key=lambda x: ("ABCD".find(x[0]) if x and x[0] in "ABCD" else 99, int(x[1:]) if len(x) > 1 and x[1:].isdigit() else 99))
if not criteria:
    st.warning("Ngân hàng này chưa có tiêu chí chấm điểm.")
    st.stop()
with col_criterion:
    with st.container(key="audit_criterion_selector"):
        icon_col, criterion_col = st.columns([1, 4], gap="small", vertical_alignment="center")
        with criterion_col:
            criterion = st.selectbox("📋 Chọn tiêu chí cần kiểm tra", criteria, key="audit_criterion")
        with icon_col:
            st.markdown('<div class="hm-criterion-icon" aria-hidden="true">📑</div>', unsafe_allow_html=True)
score_rows = bank_scores[bank_scores["criterion"] == criterion]
evidence_rows = evidence[(evidence["bank"] == bank) & (evidence["criterion"] == criterion)].copy()
if score_rows.empty:
    st.error("Không tìm thấy kết quả chấm điểm.")
    st.stop()
detail = score_rows.iloc[0]
heading(f"🌿 {bank} — {criterion}: {detail['criterion_name']}")
score = detail["final_score"]
cols = st.columns(3)
for col, (label, value, color) in zip(cols, [
    ("🧾 Điểm chấm", f"{score:g}/2" if pd.notna(score) else "Thiếu", "pink"),
    ("📚 Số bằng chứng được chọn", len(evidence_rows), "blue"),
    ("📄 Số báo cáo liên quan", evidence_rows["filename"].nunique(), "green"),
]):
    with col:
        kpi(label, value, color)

left, right = st.columns([1, 1.1], gap="medium")
with left:
    heading("🌺 Giải thích kết quả chấm điểm")
    body = f'<p><strong>Quy tắc chấm điểm (rubric)</strong></p><p>{safe(detail["rubric"])}</p>'
    body += f'<p><strong>Lý do chấm điểm tự động</strong></p><p>{safe(detail["reason"])}</p>'
    if "confidence" in detail.index:
        body += f'<p><strong>Độ tin cậy:</strong> {safe(detail["confidence"])}</p>'
    if "review_priority" in detail.index:
        body += f'<p><strong>Mức ưu tiên rà soát:</strong> {safe(detail["review_priority"])}</p>'
    card("🌸 Căn cứ chấm điểm", body, "pink")
    if "warning" in detail.index and pd.notna(detail["warning"]) and str(detail["warning"]).strip():
        st.warning(str(detail["warning"]))

with right:
    heading("📋 Danh sách bằng chứng liên quan")
    if evidence_rows.empty:
        st.warning("Chưa tìm thấy bằng chứng được chọn cho ngân hàng và tiêu chí này.")
    else:
        evidence_rows = evidence_rows.reset_index(drop=True)
        evidence_rows.insert(0, "evidence_no", range(1, len(evidence_rows) + 1))
        table_columns = ["evidence_no", "filename", "page"]
        for optional in ("tier2_score", "confidence"):
            if optional in evidence_rows.columns:
                table_columns.append(optional)
        table(evidence_rows[table_columns])
        selected_no = st.selectbox("👁️ Chọn bằng chứng để xem nội dung", evidence_rows["evidence_no"].tolist(), format_func=lambda n: f"Bằng chứng #{n}")
        ev = evidence_rows[evidence_rows["evidence_no"] == selected_no].iloc[0]
        body = f'<p><strong>Nguồn báo cáo:</strong> {safe(ev["filename"])}</p><p><strong>Trang tài liệu:</strong> {safe(ev["page"])}</p>'
        if "tier2_score" in ev.index:
            body += f'<p><strong>Điểm lọc tầng 2:</strong> {safe(ev["tier2_score"])}</p>'
        card("📑 Thông tin tài liệu", body, "yellow")

if not evidence_rows.empty:
    excerpt_col, reason_col = st.columns([1.35, 1], gap="medium")
    with excerpt_col:
        heading("📘 Nội dung bằng chứng")
        st.text_area("Trích đoạn", value=str(ev["context"]) if pd.notna(ev["context"]) else "", height=205, disabled=True)
    with reason_col:
        heading("💡 Giải thích chọn bằng chứng")
        reason = str(ev["reason"]) if "reason" in ev.index and pd.notna(ev["reason"]) else "Chưa có giải thích chọn bằng chứng."
        card("🌱 Lý do lựa chọn", f"<p>{html.escape(reason)}</p>", "green")

heading("📊 Tổng quan liên kết điểm số – bằng chứng")
evidence_counts = evidence.groupby(["bank", "criterion"]).size().reset_index(name="evidence_count")
try:
    audit = scores.merge(evidence_counts, on=["bank", "criterion"], how="left", validate="one_to_one")
except pd.errors.MergeError as exc:
    st.error(f"Không thể tổng hợp do dữ liệu chấm điểm bị trùng khóa: {exc}")
    st.stop()
audit["evidence_count"] = audit["evidence_count"].fillna(0).astype(int)
audit["traceability"] = audit["evidence_count"].apply(lambda n: "Có bằng chứng để rà soát" if n > 0 else "Chưa có bằng chứng liên kết")
cols = st.columns(3)
for col, (label, value, color) in zip(cols, [
    ("📊 Tổng kết quả chấm", len(audit), "pink"),
    ("🔗 Có bằng chứng liên kết", int((audit["evidence_count"] > 0).sum()), "green"),
    ("⚠️ Chưa có bằng chứng liên kết", int((audit["evidence_count"] == 0).sum()), "yellow"),
]):
    with col:
        kpi(label, value, color)
audit_display = audit[["bank", "criterion", "criterion_name", "final_score", "evidence_count", "traceability"]].rename(columns={
    "bank": "Ngân hàng", "criterion": "Tiêu chí", "criterion_name": "Tên tiêu chí", "final_score": "Điểm", "evidence_count": "Số bằng chứng", "traceability": "Khả năng truy xuất"
})
table(audit_display)
st.caption("Nguồn: processed_scores.csv và selected_evidence.csv. Khả năng truy xuất chỉ xác nhận sự tồn tại của bằng chứng liên kết, không xác nhận điểm chấm đúng.")
missing_evidence = audit[audit["evidence_count"] == 0].copy()
if not missing_evidence.empty:
    st.error(f"Phát hiện {len(missing_evidence)} kết quả chấm điểm chưa có bằng chứng liên kết.")
    table(missing_evidence[["bank", "criterion", "criterion_name", "final_score"]].rename(columns={"bank": "Ngân hàng", "criterion": "Tiêu chí", "criterion_name": "Tên tiêu chí", "final_score": "Điểm đã chấm"}))
else:
    st.success("Tất cả kết quả chấm điểm đều có ít nhất một bằng chứng liên kết.")
