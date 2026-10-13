import base64

import io

import html

from pathlib import Path



import pandas as pd

import streamlit as st

from utils.theme import apply_theme



st.set_page_config(page_title="Data Validation | HerMetrics", page_icon="🛡️", layout="wide")



# Only one shared sidebar. Do not create another menu here.

from hermetrics_sidebar import render as _hm_render

ROOT = Path(__file__).resolve().parent.parent

_hm_render(ROOT, show_nav=True)

apply_theme()



DATA_DIR = ROOT / "data"

ART_DIR = ROOT / "assets" / "vietnam_art"

BANKS = ["BIDV", "MB", "OCB", "VCB", "VietinBank"]

CRITERIA = [f"{p}{i}" for p in "ABCD" for i in range(1, 5)]

TOL = 1e-6





def locate_image(filename):

    """Prefer exact asset path; tolerate an accidentally nested project folder."""

    direct = ART_DIR / filename

    if direct.is_file():

        return direct

    matches = sorted(ROOT.rglob(filename), key=lambda p: (len(p.parts), str(p)))

    return matches[0] if matches else None





def image_uri(path):

    if path is None:

        return ""

    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"

    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"





hero = locate_image("data_validation_hero.jpg")

sidebar_art = locate_image("data_validation_sidebar.png")

pdf_art = locate_image("data_validation_pdf.jpg")

hero_uri = image_uri(hero)

side_uri = image_uri(sidebar_art)

pdf_uri = image_uri(pdf_art)




st.markdown("""

<style>

.stApp {background: linear-gradient(120deg,#fffaf8 0%,#f7fcfc 55%,#fffdfa 100%);}

[data-testid="stSidebar"] {background:#fffdf9 !important;}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] {display:none!important;}

h1,h2,h3 {color:#08716f!important;}

.block-container {padding-top:1.2rem;}

.hm-dv-hero {
    min-height: 230px;
    border: 1px solid #d5e8e4;
    border-radius: 19px;
    overflow: hidden;
    background-repeat: no-repeat;
    background-size: 100% 100%, 100% auto;
    background-position: center center, center 82%;
    display: flex;
    align-items: center;
    padding: 24px 28px;
    box-shadow: 0 8px 22px #1b655015;
    margin-bottom: 16px;
}
@media (max-width: 700px) {
    .hm-dv-hero {min-height: 210px; background-size: 100% 100%, auto 125%; background-position: center, 49% 80%;}
}
.hm-dv-eyebrow {color:#8e1745;font-size:11px;font-weight:800;letter-spacing:2px;}

.hm-dv-title {font-family:Georgia,serif;font-weight:800;font-size:clamp(27px,3vw,43px);line-height:1.15;color:#861239;margin:5px 0;}

.hm-dv-sub {font-size:14px;color:#355b67;max-width:650px;}

.hm-dv-section {font-size:21px;font-weight:850;color:#096b68;margin:18px 0 10px;}

/* Four pastel KPI cards matching the approved design */
.hm-dv-kpi {position:relative;isolation:isolate;overflow:hidden;box-sizing:border-box;
 border:2px solid var(--kpi-border);border-radius:17px;padding:17px 17px 16px;
 min-height:155px;background:linear-gradient(145deg,var(--kpi-bg),#fff 85%);
 box-shadow:0 8px 22px rgba(29,68,75,.07);}
.hm-dv-kpi::after {content:"";position:absolute;width:145px;height:145px;border-radius:50%;
 right:-75px;bottom:-91px;border:24px solid var(--kpi-ring);opacity:.55;z-index:-1;}
.hm-dv-kpi-top {display:flex;align-items:center;gap:10px;min-height:43px;}
.hm-dv-kpi-icon {display:flex;align-items:center;justify-content:center;flex:0 0 42px;
 width:42px;height:42px;border-radius:50%;background:var(--kpi-icon-bg);
 color:var(--kpi-color);font-size:22px;font-weight:800;}
.hm-dv-kpi-label {font-size:14px;line-height:1.3;color:#18344b;font-weight:800;}
.hm-dv-kpi-value {margin-top:12px;font-size:43px;font-family:Georgia,serif;
 color:var(--kpi-color);font-weight:800;line-height:1.1;}
.hm-dv-kpi--green {--kpi-border:#8bdec3;--kpi-bg:#effcf6;--kpi-icon-bg:#d7f6e9;--kpi-color:#086b52;--kpi-ring:#c6f3e5;}
.hm-dv-kpi--pink {--kpi-border:#f4a4c3;--kpi-bg:#fff2f7;--kpi-icon-bg:#fbd9e6;--kpi-color:#aa164d;--kpi-ring:#f9d5e5;}
.hm-dv-kpi--yellow {--kpi-border:#f5d27c;--kpi-bg:#fffbef;--kpi-icon-bg:#fff0c7;--kpi-color:#9c6600;--kpi-ring:#ffebba;}
.hm-dv-kpi--blue {--kpi-border:#9dccff;--kpi-bg:#f1f8ff;--kpi-icon-bg:#dceeff;--kpi-color:#1256af;--kpi-ring:#d1e7ff;}
@media(max-width:700px){.hm-dv-kpi {min-height:140px;padding:13px;}.hm-dv-kpi-value{font-size:36px;}.hm-dv-kpi-label{font-size:12px;}}

.hm-dv-table {border:1px solid #cfe5e3;border-radius:13px;overflow:auto;margin-bottom:16px;background:white;box-shadow:0 3px 12px #0b65500b;}

.hm-dv-table table {border-collapse:collapse;width:100%;font-size:13px;}

.hm-dv-table th {background:#108580;color:white;text-align:left;padding:12px 11px;white-space:nowrap;}

.hm-dv-table td {padding:9px 11px;border-bottom:1px solid #e3eded;color:#294d5d;}

.hm-dv-table tr:nth-child(even) td {background:#eff7f9;}

.hm-dv-table tr:last-child td {border-bottom:none;}

.hm-dv-pdf {border:1px solid #cde7df;border-radius:18px;padding:20px;

 background:linear-gradient(100deg,#fffdf8eF,#f3faf9dE);margin-top:12px;}

.hm-dv-pdf-title {font-size:23px;font-weight:850;color:#08746e;}

.hm-dv-note {font-size:12px;color:#70818c;}

</style>

""", unsafe_allow_html=True)



if sidebar_art:

    # Place illustration below the single shared HerMetrics navigation.

    with st.sidebar:

        st.image(str(sidebar_art), use_container_width=True)



@st.cache_data(show_spinner=False)

def load_data():

    filenames = {"ranking": "ranking.csv", "scores": "processed_scores.csv", "pillars": "pillar_scores.csv", "evidence": "selected_evidence.csv"}

    return {key: pd.read_csv(DATA_DIR / name, encoding="utf-8-sig") for key, name in filenames.items()}



try:

    data = load_data()

except Exception as exc:

    st.error(f"Không đọc được dữ liệu CSV: {exc}")

    st.stop()



ranking, scores, pillars, evidence = [data[k].copy() for k in ("ranking", "scores", "pillars", "evidence")]

required = {

    "ranking.csv": (ranking, ["bank", "rank", "BDTI", "A", "B", "C", "D"]),

    "processed_scores.csv": (scores, ["bank", "criterion", "pillar", "final_score"]),

    "pillar_scores.csv": (pillars, ["bank", "pillar", "pillar_score"]),

    "selected_evidence.csv": (evidence, ["bank", "criterion"]),

}

for filename, (frame, cols) in required.items():

    missing = [col for col in cols if col not in frame.columns]

    if missing:

        st.error(f"{filename} thiếu cột: {', '.join(missing)}")

        st.stop()

for frame in (ranking, scores, pillars, evidence):

    frame["bank"] = frame["bank"].astype("string").str.strip()

for frame in (scores, evidence):

    frame["criterion"] = frame["criterion"].astype("string").str.strip()

scores["pillar"] = scores["pillar"].astype("string").str.strip()

pillars["pillar"] = pillars["pillar"].astype("string").str.strip()

for frame, cols in ((scores, ["final_score"]), (pillars, ["pillar_score"]), (ranking, ["rank", "BDTI", "A", "B", "C", "D"])):

    for col in cols:

        frame[col] = pd.to_numeric(frame[col], errors="coerce")



issues = []

def add_issue(group, detail):

    issues.append({"Nhóm kiểm tra": group, "Chi tiết": detail})



for name, frame, count in (("Ranking", ranking, 5), ("Scores", scores, 80), ("Pillars", pillars, 20)):

    if len(frame) != count:

        add_issue(name, f"Có {len(frame)} dòng, cần {count}.")

for name, frame, keys in (("Ranking", ranking, ["bank"]), ("Scores", scores, ["bank", "criterion"]), ("Pillars", pillars, ["bank", "pillar"])):

    duplicates = frame.duplicated(keys, keep=False)

    if duplicates.any():

        add_issue(name, f"Có {int(duplicates.sum())} dòng trùng khóa.")



expected = pd.MultiIndex.from_product([BANKS, CRITERIA], names=["bank", "criterion"])

actual = pd.MultiIndex.from_frame(scores[["bank", "criterion"]].dropna())

for bank, criterion in expected.difference(actual):

    add_issue("Thiếu tiêu chí", f"{bank} – {criterion}")

for bank, criterion in actual.difference(expected):

    add_issue("Tiêu chí không hợp lệ", f"{bank} – {criterion}")

if set(ranking["bank"].dropna()) != set(BANKS):

    add_issue("Ranking", "Danh sách ngân hàng không đúng.")



for _, r in scores.loc[~scores["final_score"].isin([0, 1, 2])].iterrows():

    add_issue("Điểm không hợp lệ", f"{r['bank']} – {r['criterion']}: {r['final_score']}")

wrong = scores.loc[(scores["pillar"] != scores["criterion"].str[0]).fillna(True)]

for _, r in wrong.iterrows():

    add_issue("Sai trụ cột", f"{r['bank']} – {r['criterion']}: {r['pillar']}")



calculated_pillars = scores.groupby(["bank", "pillar"], as_index=False).agg(

    raw_score=("final_score", "sum"), count=("criterion", "nunique"), valid_count=("final_score", "count")

)

calculated_pillars["calculated_score"] = calculated_pillars["raw_score"] / 8 * 100

try:

    pillar_check = calculated_pillars.merge(pillars[["bank", "pillar", "pillar_score"]], on=["bank", "pillar"], how="outer", validate="one_to_one")

except pd.errors.MergeError as exc:

    st.error(f"Không thể đối chiếu điểm trụ cột do khóa trùng: {exc}")

    st.stop()

for _, r in pillar_check.iterrows():

    bank, p = r["bank"], r["pillar"]

    if pd.isna(r["calculated_score"]) or pd.isna(r["pillar_score"]):

        add_issue("Điểm trụ cột", f"{bank} – {p}: thiếu dữ liệu.")

    elif abs(r["calculated_score"] - r["pillar_score"]) > TOL:

        add_issue("Sai điểm trụ cột", f"{bank} – {p}: tính lại {r['calculated_score']:.3f}, file {r['pillar_score']:.3f}")

    if pd.notna(r["count"]) and (r["count"] != 4 or r["valid_count"] != 4):

        add_issue("Thiếu điểm trụ cột", f"{bank} – {p}: chưa đủ 4 điểm hợp lệ.")



bdti_calc = scores.groupby("bank", as_index=False).agg(total_score=("final_score", "sum"), valid_count=("final_score", "count"))

bdti_calc["BDTI_tinh_lai"] = bdti_calc["total_score"] / 32 * 100

try:

    bdti_check = ranking.merge(bdti_calc, on="bank", how="outer", validate="one_to_one")

except pd.errors.MergeError as exc:

    st.error(f"Không thể đối chiếu BDTI do khóa trùng: {exc}")

    st.stop()

for _, r in bdti_check.iterrows():

    bank = r["bank"]

    if pd.isna(r["valid_count"]) or r["valid_count"] != 16:

        add_issue("BDTI", f"{bank}: thiếu điểm tiêu chí.")

    elif pd.isna(r["BDTI"]) or abs(r["BDTI"] - r["BDTI_tinh_lai"]) > TOL:

        add_issue("Sai BDTI", f"{bank}: BDTI không khớp.")

    pv = [r[p] for p in "ABCD"]

    if any(pd.isna(x) for x in pv):

        add_issue("BDTI", f"{bank}: thiếu điểm trụ cột.")

    elif pd.notna(r["BDTI"]) and abs(sum(pv) / 4 - r["BDTI"]) > TOL:

        add_issue("Sai BDTI", f"{bank}: trung bình 4 trụ cột không khớp.")

    for p in "ABCD":

        matched = calculated_pillars[(calculated_pillars["bank"] == bank) & (calculated_pillars["pillar"] == p)]

        if len(matched) == 1 and pd.notna(r[p]) and abs(r[p] - matched.iloc[0]["calculated_score"]) > TOL:

            add_issue("Sai điểm Ranking", f"{bank} – {p}: không khớp điểm tiêu chí.")

if ranking["BDTI"].notna().all():

    expected_rank = ranking["BDTI"].rank(method="min", ascending=False)

    for idx, r in ranking.iterrows():

        if pd.isna(r["rank"]) or r["rank"] != expected_rank.loc[idx]:

            add_issue("Sai thứ hạng", f"{r['bank']}: hạng {r['rank']}, dự kiến {expected_rank.loc[idx]:.0f}")



evidence_counts = evidence.groupby(["bank", "criterion"]).size().reset_index(name="evidence_count")

audit = scores.merge(evidence_counts, on=["bank", "criterion"], how="left", validate="one_to_one")

audit["evidence_count"] = audit["evidence_count"].fillna(0).astype(int)

unlinked = audit[audit["evidence_count"] == 0].copy()





def table(frame, max_height=None):

    safe = frame.copy().astype(object).where(pd.notna(frame), "—")

    markup = safe.to_html(index=False, escape=True, border=0, classes="hm-table")

    height = f'max-height:{max_height}px;' if max_height else ''

    st.markdown(f'<div class="hm-dv-table" style="{height}">{markup}</div>', unsafe_allow_html=True)





def section(text):

    st.markdown(f'<div class="hm-dv-section">{html.escape(text)}</div>', unsafe_allow_html=True)



hero_bg = (
    "linear-gradient(90deg,rgba(255,253,248,.97) 0%,"
    "rgba(255,253,248,.82) 27%,"
    "rgba(255,253,248,.10) 54%,"
    "rgba(255,253,248,0) 76%),"
    f"url('{hero_uri}')"
    if hero_uri
    else "linear-gradient(110deg,#fffaf2,#cde9f6,#e2f4dc)"
)

st.markdown(f'''<div class="hm-dv-hero" style="background-image:{hero_bg}">

<div><div class="hm-dv-eyebrow">HERMETRICS · BANKING INTELLIGENCE</div>

<div class="hm-dv-title">🛡️ DATA VALIDATION</div>

<div class="hm-dv-sub">Kiểm tra dữ liệu, phát hiện thiếu sót và đảm bảo tính nhất quán trước khi phân tích.</div></div></div>''', unsafe_allow_html=True)



section("📚 Tổng quan kiểm tra")

kpis = [
    ("green", "🏦", "Ngân hàng", ranking["bank"].nunique()),
    ("pink", "📋", "Kết quả chấm", len(scores)),
    ("yellow", "⚠️", "Vấn đề dữ liệu", len(issues)),
    ("blue", "🔗", "Thiếu liên kết bằng chứng", len(unlinked)),
]

for col, (color, symbol, label, value) in zip(st.columns(4), kpis):
    with col:
        st.markdown(
            f'<div class="hm-dv-kpi hm-dv-kpi--{color}">'
            f'<div class="hm-dv-kpi-top">'
            f'<span class="hm-dv-kpi-icon">{symbol}</span>'
            f'<span class="hm-dv-kpi-label">{html.escape(label)}</span>'
            f'</div><div class="hm-dv-kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )


section("🔎 Kiểm tra tính nhất quán")

if issues:

    st.error(f"Phát hiện {len(issues)} vấn đề cần xử lý.")

    table(pd.DataFrame(issues), 290)

else:

    st.success("Không phát hiện sai lệch cấu trúc, điểm số hoặc công thức BDTI trong các phép kiểm tra.")



section("📊 Đối chiếu BDTI")

bdti_display = bdti_check[["bank", "rank", "BDTI", "BDTI_tinh_lai", "total_score", "valid_count"]].rename(columns={

    "bank": "Ngân hàng", "rank": "Hạng", "BDTI": "BDTI (xếp hạng)", "BDTI_tinh_lai": "BDTI (tính lại)",

    "total_score": "Tổng điểm /32", "valid_count": "Số điểm hợp lệ"

})

table(bdti_display.round(3))



section("📈 Đối chiếu điểm 4 trụ cột")

pillar_display = pillar_check.rename(columns={

    "bank": "Ngân hàng", "pillar": "Trụ cột", "raw_score": "Điểm gốc (raw)", "count": "Số tiêu chí",

    "valid_count": "Số tiêu chí hợp lệ", "calculated_score": "Điểm tính toán", "pillar_score": "Điểm trụ cột"

})

table(pillar_display.round(3), 310)



section("⚠️ Trường hợp thiếu bằng chứng liên kết")

if unlinked.empty:

    st.success("Tất cả tiêu chí đều có bằng chứng liên kết.")

else:

    st.warning(f"Có {len(unlinked)} tiêu chí chưa có bằng chứng liên kết. Không tự động thay đổi điểm số.")

    table(unlinked[["bank", "criterion", "final_score", "evidence_count"]].rename(columns={

        "bank": "Ngân hàng", "criterion": "Tiêu chí", "final_score": "Điểm cuối cùng", "evidence_count": "Số bằng chứng"

    }), 260)



section("📄 Xuất báo cáo kiểm tra")



# PDF generation is intentionally isolated: CSV validation remains usable if ReportLab is absent.

def create_pdf():

    from reportlab.lib import colors

    from reportlab.lib.enums import TA_CENTER

    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    from reportlab.lib.pagesizes import A4

    from reportlab.lib.utils import ImageReader

    from reportlab.pdfbase import pdfmetrics

    from reportlab.pdfbase.ttfonts import TTFont

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image



    fonts = [

        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),

        Path("C:/Windows/Fonts/arial.ttf"),

        Path("C:/Windows/Fonts/tahoma.ttf"),

    ]

    regular = next((f for f in fonts if f.exists()), None)

    if regular:

        pdfmetrics.registerFont(TTFont("HMUnicode", str(regular)))

        font_name = "HMUnicode"

    else:

        # Fallback still creates a PDF; accented characters require a Unicode font installed.

        font_name = "Helvetica"

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("HMTitle", parent=styles["Title"], fontName=font_name, fontSize=20, leading=27, textColor=colors.HexColor("#087570"), spaceAfter=10)

    subtitle_style = ParagraphStyle("HMSub", parent=styles["Normal"], fontName=font_name, fontSize=10, leading=15, textColor=colors.HexColor("#425f6c"), spaceAfter=12)

    heading_style = ParagraphStyle("HMHeading", parent=styles["Heading2"], fontName=font_name, fontSize=12, leading=18, textColor=colors.HexColor("#087570"), spaceBefore=16, spaceAfter=8)

    cell_style = ParagraphStyle("HMCell", fontName=font_name, fontSize=7, leading=10, textColor=colors.HexColor("#254758"))

    head_style = ParagraphStyle("HMHead", parent=cell_style, textColor=colors.white, fontSize=7)

    output = io.BytesIO()

    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=35, leftMargin=35, topMargin=38, bottomMargin=40)

    usable = A4[0] - 70

    story = []

    if pdf_art:

        try:

            from PIL import Image as PILImage

            with PILImage.open(pdf_art) as im:

                w, h = im.size

            display_h = min(115, usable * h / w)

            story.append(Image(str(pdf_art), width=usable, height=display_h))

            story.append(Spacer(1, 12))

        except Exception:

            pass

    story += [Paragraph("HerMetrics | DATA VALIDATION REPORT", title_style),

              Paragraph("Báo cáo kiểm tra tính nhất quán dữ liệu · 2025", subtitle_style)]

    def pdf_table(df, widths=None, limit=None):

        if limit is not None:

            df = df.head(limit)

        headers = [Paragraph(html.escape(str(c)), head_style) for c in df.columns]

        rows = [headers]

        for values in df.itertuples(index=False, name=None):

            rows.append([Paragraph(html.escape(str(v)), cell_style) for v in values])

        if widths is None:

            widths = [usable / len(df.columns)] * len(df.columns)

        t = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")

        t.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#11847e")),

            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef8f8")]),

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("LEFTPADDING", (0, 0), (-1, -1), 7),

            ("RIGHTPADDING", (0, 0), (-1, -1), 7),

            ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#d7e9e6")),

        ]))

        return t

    overview = pd.DataFrame([

        ("Ngân hàng", ranking["bank"].nunique()), ("Kết quả chấm", len(scores)),

        ("Vấn đề dữ liệu", len(issues)), ("Thiếu liên kết bằng chứng", len(unlinked))

    ], columns=["Chỉ số", "Giá trị"])

    story += [Paragraph("Tổng quan kiểm tra", heading_style), pdf_table(overview, [usable * .75, usable * .25])]

    story += [Paragraph("Đối chiếu BDTI", heading_style), pdf_table(bdti_display.round(3))]

    story += [Paragraph("Đối chiếu điểm 4 trụ cột", heading_style), pdf_table(pillar_display.round(3))]

    story.append(Paragraph("Trường hợp thiếu bằng chứng liên kết", heading_style))

    if unlinked.empty:

        story.append(Paragraph("Không có trường hợp thiếu bằng chứng liên kết.", subtitle_style))

    else:

        story.append(pdf_table(unlinked[["bank", "criterion", "final_score", "evidence_count"]].rename(columns={

            "bank": "Ngân hàng", "criterion": "Tiêu chí", "final_score": "Điểm", "evidence_count": "Bằng chứng"

        })))

    story.append(Paragraph("Kết quả kiểm tra tính nhất quán", heading_style))

    if issues:

        story.append(pdf_table(pd.DataFrame(issues), [usable * .28, usable * .72]))

    else:

        story.append(Paragraph("Không phát hiện sai lệch trong các phép kiểm tra đã thực hiện.", subtitle_style))

    story.append(Spacer(1, 12))

    story.append(Paragraph("Nguồn: các file CSV của nhóm. Kiểm tra dữ liệu không thay thế việc xác minh độc lập nội dung bằng chứng và rubric.", subtitle_style))

    def footer(canvas, document):

        canvas.saveState()

        canvas.setStrokeColor(colors.HexColor("#b8dbd6"))

        canvas.line(35, 31, A4[0] - 35, 31)

        canvas.setFont(font_name, 8)

        canvas.setFillColor(colors.HexColor("#667c88"))

        canvas.drawString(35, 19, "HerMetrics · Banking Intelligence 2025")

        canvas.drawRightString(A4[0] - 35, 19, str(document.page))

        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)

    return output.getvalue()



pdf_banner = (f"linear-gradient(90deg,rgba(248,255,251,.97),rgba(248,255,251,.79) 56%,rgba(248,255,251,.04)),url('{pdf_uri}')" if pdf_uri else "linear-gradient(110deg,#e3f5f0,#d9edf3,#fff2ce)")

st.markdown(f'''

<style>

.hm-pdf-studio {{border:1px solid #b9dfd5;border-radius:19px;overflow:hidden;margin:14px 0 16px;box-shadow:0 10px 28px #145b4b15;}}

.hm-pdf-studio-banner {{min-height:165px;padding:28px 30px;display:flex;flex-direction:column;justify-content:center;background-image:{pdf_banner};background-position:center right;background-size:cover;}}

.hm-pdf-eyebrow {{font-size:11px;font-weight:850;letter-spacing:2px;color:#8b1745;}}

.hm-pdf-heading {{font-family:Georgia,serif;font-weight:800;font-size:clamp(26px,3vw,39px);color:#086d66;line-height:1.2;margin:6px 0;}}

.hm-pdf-desc {{font-size:13px;color:#385e63;max-width:530px;}}

.hm-pdf-preview-caption {{color:#176f68;font-weight:800;font-size:16px;margin:12px 0 8px;}}

</style>

<div class="hm-pdf-studio"><div class="hm-pdf-studio-banner">

<div class="hm-pdf-eyebrow">HERMETRICS · REPORT COLLECTION</div>

<div class="hm-pdf-heading">DATA VALIDATION REPORT</div>

<div class="hm-pdf-desc">Xem trước từng trang của báo cáo kiểm tra dữ liệu trước khi xuất PDF.</div>

</div></div>''', unsafe_allow_html=True)

# Style only the two PDF action buttons, not navigation controls.
st.markdown("""
<style>
div.stButton > button[kind="primary"] {
    background: #16834A !important;
    border: 1px solid #106B3B !important;
    color: #FFFFFF !important;
    border-radius: 11px !important;
    min-height: 48px !important;
    box-shadow: 0 4px 12px rgba(22,131,74,.20);
}
div.stButton > button[kind="primary"]:hover {
    background: #106B3B !important;
    color: #FFFFFF !important;
}
div.stDownloadButton > button {
    background: #1764C0 !important;
    border: 1px solid #1052A0 !important;
    color: #FFFFFF !important;
    border-radius: 11px !important;
    min-height: 48px !important;
    box-shadow: 0 4px 12px rgba(23,100,192,.20);
}
div.stDownloadButton > button:hover {
    background: #1052A0 !important;
    color: #FFFFFF !important;
}
div.stButton > button[kind="primary"] p,
div.stDownloadButton > button p {
    color: #FFFFFF !important;
    font-size: 16px !important;
    font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)

try:

    pdf_bytes = create_pdf()

    left, right = st.columns(2)

    with left:

        if st.button("👁️ Xem trước PDF" if not st.session_state.get("hm_dv_show_pdf", False) else "✖ Đóng bản xem trước", use_container_width=True, type="primary"):

            st.session_state["hm_dv_show_pdf"] = not st.session_state.get("hm_dv_show_pdf", False)

            st.session_state["hm_dv_pdf_page"] = 0

    with right:

        st.download_button("📥 Tải báo cáo PDF", data=pdf_bytes, file_name="HerMetrics_Data_Validation_2025.pdf", mime="application/pdf", use_container_width=True)



    if st.session_state.get("hm_dv_show_pdf", False):

        try:

            import fitz  # PyMuPDF: render the exact PDF bytes that will be downloaded.

        except ImportError:

            st.info("Để xem trước từng trang, cài PyMuPDF: .venv/Scripts/python.exe -m pip install pymupdf")

        else:

            st.markdown('<div class="hm-pdf-preview-caption">📖 XEM TRƯỚC BÁO CÁO</div>', unsafe_allow_html=True)

            with fitz.open(stream=pdf_bytes, filetype="pdf") as preview_doc:

                total_pages = len(preview_doc)

                page_no = min(max(int(st.session_state.get("hm_dv_pdf_page", 0)), 0), total_pages - 1)

                previous, indicator, following = st.columns([1, 2, 1])

                with previous:

                    if st.button("← Trang trước", disabled=page_no == 0, use_container_width=True, key="hm_dv_prev"):

                        page_no -= 1

                        st.session_state["hm_dv_pdf_page"] = page_no

                with indicator:

                    st.markdown(f'<div style="text-align:center;color:#08746e;font-weight:800;padding:10px">TRANG {page_no + 1} / {total_pages}</div>', unsafe_allow_html=True)

                with following:

                    if st.button("Trang sau →", disabled=page_no >= total_pages - 1, use_container_width=True, key="hm_dv_next"):

                        page_no += 1

                        st.session_state["hm_dv_pdf_page"] = page_no

                preview_page = preview_doc.load_page(page_no)

                pix = preview_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)

                st.image(pix.tobytes("png"), use_container_width=True)

                st.caption("Bản xem trước được dựng trực tiếp từ chính file PDF tải xuống. Có thể chuyển trang bằng các nút phía trên.")

except ImportError as exc:

    st.warning(f"Thiếu thư viện để xuất PDF: {exc}. Cài bằng: .venv/Scripts/python.exe -m pip install reportlab pillow pymupdf")

except Exception as exc:

    st.error(f"Không tạo được PDF: {exc}")
