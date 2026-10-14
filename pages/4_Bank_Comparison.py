"""HerMetrics · So sánh ngân hàng | Trang phân tích độc lập."""



from __future__ import annotations



import base64



import html



from pathlib import Path



import numpy as np



import pandas as pd



import plotly.express as px



import plotly.graph_objects as go



import streamlit as st



from utils.theme import apply_theme



st.set_page_config(page_title="So sánh ngân hàng | HerMetrics", page_icon="⚖️", layout="wide")



# Exactly one shared navigation menu. Only Bank Comparison adds its own sidebar artwork.



from hermetrics_sidebar import render as _hm_render



ROOT = Path(__file__).resolve().parent.parent



_hm_render(ROOT, show_nav=True)



apply_theme()



DATA = ROOT / "data"



ART = ROOT / "assets" / "vietnam_art"



HERO = ART / "bank_comparison_nhatrang_hero.jpg"



SIDE = ART / "bank_comparison_nhatrang_sidebar.jpg"



COLORS = {"OCB": "#70B852", "MB": "#3B99EC", "BIDV": "#E7B03B", "VietinBank": "#2AA8A0", "VCB": "#D66F65"}



PILLARS = {"A": "Chiến lược & nguồn lực số", "B": "Sản phẩm số & trải nghiệm khách hàng", "C": "Công nghệ & dữ liệu", "D": "Vận hành số & an toàn"}



def data_url(path: Path) -> str:



    if not path.is_file():



        return ""



    suffix = {".png": "png", ".webp": "webp"}.get(path.suffix.lower(), "jpeg")



    return f"data:image/{suffix};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"



@st.cache_data(show_spinner=False)



def load_data():



    ranking = pd.read_csv(DATA / "ranking.csv", encoding="utf-8-sig")



    scores = pd.read_csv(DATA / "processed_scores.csv", encoding="utf-8-sig")



    required_r = {"bank", "rank", "BDTI", "A", "B", "C", "D"}



    required_s = {"bank", "criterion", "final_score"}



    if not required_r.issubset(ranking.columns):



        raise ValueError(f"ranking.csv thiếu cột: {sorted(required_r - set(ranking.columns))}")



    if not required_s.issubset(scores.columns):



        raise ValueError(f"processed_scores.csv thiếu cột: {sorted(required_s - set(scores.columns))}")



    ranking["bank"] = ranking["bank"].astype(str).str.strip()



    scores["bank"] = scores["bank"].astype(str).str.strip()



    scores["criterion"] = scores["criterion"].astype(str).str.strip().str.upper()



    for col in ["rank", "BDTI", "A", "B", "C", "D"]:



        ranking[col] = pd.to_numeric(ranking[col], errors="coerce")



    scores["final_score"] = pd.to_numeric(scores["final_score"], errors="coerce")



    return ranking.sort_values("rank"), scores



st.markdown("""



<style>



.stApp {background:linear-gradient(180deg,#fbfefd 0%,#fffdfa 45%,#f9fcff 100%);}



[data-testid="stSidebar"] {background:#fffdf9!important;}



[data-testid="stSidebarNav"] {display:none!important;}



.hm-bc-hero{height:205px;position:relative;overflow:hidden;border-radius:17px;



 border:1px solid #dcebe7;background:linear-gradient(110deg,#f8fff6,#d5f0ff);



 box-shadow:0 6px 19px rgba(29,89,110,.08);margin-bottom:15px;}



.hm-bc-hero-art{position:absolute;inset:0 0 0 38%;background-size:cover;background-position:center 48%;}



.hm-bc-hero:after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#fffdf5 0%,rgba(255,253,245,.97) 27%,rgba(255,253,245,.76) 45%,transparent 75%);pointer-events:none;}



.hm-bc-hero-copy{position:relative;z-index:1;padding:30px 36px;max-width:68%;}



.hm-bc-eyebrow{font:800 11px 'Be Vietnam Pro',sans-serif;letter-spacing:2.2px;color:#8c1b48;}



.hm-bc-title{font:800 clamp(27px,3.3vw,46px)/1.14 'Playfair Display',Georgia,serif;color:#81153c;margin:10px 0;}



.hm-bc-sub{font:600 12px 'Be Vietnam Pro',sans-serif;color:#345669;}



.hm-bc-side-art{margin:26px 0 12px;border-radius:12px;overflow:hidden;border:1px solid #d6e8e2;}



.hm-bc-side-art img{display:block;width:100%;max-height:320px;object-fit:cover;object-position:center;}



.hm-bc-section{font:800 19px 'Be Vietnam Pro',sans-serif;color:#155d51;margin:19px 0 10px;}



.hm-bc-card{border:1px solid #dce8e0;border-radius:15px;background:rgba(255,255,255,.94);padding:12px 17px;margin:5px 0 12px;}



.hm-bc-kpi{border-radius:15px;padding:17px 19px;min-height:114px;border:1px solid rgba(42,100,102,.12);}



.hm-bc-kpi .label{font:700 12px 'Be Vietnam Pro',sans-serif;color:#3e6470;}



.hm-bc-kpi .number{font:800 30px 'Playfair Display',Georgia,serif;color:#7e173d;margin:7px 0 3px;}



.hm-bc-kpi .detail{font:500 11px 'Be Vietnam Pro',sans-serif;color:#496473;}



.hm-bc-kpi.yellow{background:linear-gradient(120deg,#fffaf0,#ffebbf);}



.hm-bc-kpi.blue{background:linear-gradient(120deg,#f4faff,#d9efff);}



.hm-bc-kpi.green{background:linear-gradient(120deg,#f4fff3,#dcf3d7);}



.hm-bc-select{border:1px solid #d7e7dc;border-radius:15px;padding:14px 18px 7px;background:linear-gradient(115deg,#fffefa,#f0f9ef);margin:4px 0 13px;}



[data-testid="stPlotlyChart"]{background:#fff;border:1px solid #e1ebe5;border-radius:15px;padding:6px;}



[data-testid="stDataFrame"]{border:1px solid #dbe9e3;border-radius:12px;overflow:hidden;}

/* Guaranteed header styling for the two summary tables (HTML, not canvas). */

.hm-bc-table-wrap{width:100%;overflow-x:auto;border:1px solid #c9e1db;border-radius:13px;

 background:white;box-shadow:0 3px 14px rgba(21,93,81,.055);margin:7px 0 21px;}

.hm-bc-table{width:100%;border-collapse:collapse;font:500 13px 'Be Vietnam Pro',Arial,sans-serif;min-width:590px;}

.hm-bc-table thead th{background:#126d68!important;color:#fff!important;text-align:left;

 font-weight:800;padding:14px 13px;border-right:1px solid rgba(255,255,255,.19);white-space:nowrap;}

.hm-bc-table tbody td{padding:11px 13px;border-top:1px solid #e3eeeb;color:#274d52;}

.hm-bc-table tbody tr:nth-child(even){background:#f1f9f6;}

.hm-bc-table tbody tr:hover{background:#e3f3ed;}

.hm-bc-table td.hm-num{text-align:right;font-variant-numeric:tabular-nums;}

.hm-bc-table td.hm-bank{font-weight:800;color:#155d51;}





@media(max-width:750px){.hm-bc-hero{height:180px}.hm-bc-hero-copy{padding:21px;max-width:85%}.hm-bc-title{font-size:26px}.hm-bc-sub{font-size:10px}}



</style>



""", unsafe_allow_html=True)



# Sidebar picture is rendered only on this page, not in hermetrics_sidebar.py.



if SIDE.is_file():



    with st.sidebar:



        st.markdown(f'<div class="hm-bc-side-art"><img src="{data_url(SIDE)}" alt="Tranh Nha Trang"></div>', unsafe_allow_html=True)



hero_style = f"background-image:url('{data_url(HERO)}')" if HERO.is_file() else "background:linear-gradient(120deg,#bce6fa,#fff0c5)"



st.markdown(f"""



<div class="hm-bc-hero"><div class="hm-bc-hero-art" style="{hero_style}"></div>



<div class="hm-bc-hero-copy"><div class="hm-bc-eyebrow">NGÂN HÀNG THƯƠNG MẠI VIỆT NAM</div>



<div class="hm-bc-title">SO SÁNH NGÂN HÀNG</div>



<div class="hm-bc-sub">So sánh và phân tích chuyển đổi số giữa các ngân hàng · 2025</div></div></div>



""", unsafe_allow_html=True)



try:



    ranking, scores = load_data()



except (OSError, ValueError, pd.errors.ParserError) as exc:



    st.error(f"Không đọc được dữ liệu so sánh: {exc}")



    st.stop()



banks = ranking["bank"].dropna().unique().tolist()



if len(banks) < 2:



    st.error("Cần ít nhất hai ngân hàng trong ranking.csv để so sánh.")



    st.stop()



# Selection panel: two featured banks, with optional additional banks.

LOGOS = ROOT / "assets" / "logos"



def bank_logo(bank_name: str) -> str:

    for ext in (".png", ".jpg", ".jpeg", ".webp"):

        path = LOGOS / f"{bank_name}{ext}"

        if path.is_file():

            return data_url(path)

    return ""



st.markdown("""

<style>

.hm-bc-pick-title{border:1px solid #dce9db;border-radius:13px;padding:13px 18px;

 background:linear-gradient(105deg,#f9fff6 0%,#fffefa 65%,#e1f5f7 100%);margin:5px 0 9px;}

.hm-bc-pick-title strong{font:800 19px 'Be Vietnam Pro',sans-serif;color:#235d48;}

.hm-bc-pick-title small{display:block;color:#59727b;font:500 11px 'Be Vietnam Pro',sans-serif;margin-top:3px;}

.hm-bc-bank-card{display:flex;align-items:center;gap:15px;border:1px solid #e2e8df;

 border-radius:11px;background:#fff;min-height:84px;padding:9px 15px;margin-bottom:6px;

 box-shadow:0 3px 12px rgba(40,80,75,.045);}

.hm-bc-bank-card img{width:83px;height:56px;object-fit:contain;flex-shrink:0;}

.hm-bc-bank-card .placeholder{width:83px;height:56px;display:flex;align-items:center;

 justify-content:center;background:#f2f8f5;color:#17735d;border-radius:8px;font-weight:800;}

.hm-bc-bank-card .meta{font:700 10px 'Be Vietnam Pro',sans-serif;color:#8d4760;}

.hm-bc-bank-card .name{font:800 24px 'Playfair Display',Georgia,serif;color:#87123c;margin-top:3px;}

/* Make bank selectors clearly legible. */

[data-testid="stSelectbox"] [data-baseweb="select"] > div{min-height:45px;border-radius:9px;}

[data-testid="stSelectbox"] [data-baseweb="select"] span{font-weight:700;}

</style>

""", unsafe_allow_html=True)



st.markdown('<div class="hm-bc-pick-title"><strong>🌿 Chọn ngân hàng cần so sánh</strong>'

            '<small>Lựa chọn 2 ngân hàng để xem và so sánh kết quả đánh giá</small></div>',

            unsafe_allow_html=True)



if st.session_state.get("bc_first") not in banks:

    st.session_state["bc_first"] = banks[0]

if st.session_state.get("bc_second") not in banks:

    st.session_state["bc_second"] = next(b for b in banks if b != st.session_state["bc_first"])



def swap_banks():

    st.session_state["bc_first"], st.session_state["bc_second"] = (

        st.session_state["bc_second"], st.session_state["bc_first"]

    )



col_a, col_b, col_swap = st.columns([5, 5, 0.8], vertical_alignment="bottom")

for col, state_key, label, number in (

    (col_a, "bc_first", "Ngân hàng 1", 1),

    (col_b, "bc_second", "Ngân hàng 2", 2),

):

    with col:

        bank_name = st.session_state[state_key]

        logo = bank_logo(bank_name)

        logo_markup = (f'<img src="{logo}" alt="{html.escape(bank_name)}">' if logo

                       else f'<div class="placeholder">{html.escape(bank_name)}</div>')

        st.markdown(

            f'<div class="hm-bc-bank-card">{logo_markup}<div>'

            f'<div class="meta">{label}</div>'

            f'<div class="name">{html.escape(bank_name)}</div></div></div>',

            unsafe_allow_html=True,

        )

        st.selectbox(f"Đổi {label.lower()}", banks, key=state_key)

with col_swap:

    st.button("⇄", on_click=swap_banks, help="Đảo vị trí hai ngân hàng", width="stretch")



if st.session_state["bc_first"] == st.session_state["bc_second"]:

    st.warning("Hãy chọn hai ngân hàng khác nhau.")

    st.stop()



with st.expander("＋ So sánh thêm ngân hàng (tối đa 5)"):

    extra_options = [b for b in banks if b not in

                     (st.session_state["bc_first"], st.session_state["bc_second"])]

    selected_extra = st.multiselect("Ngân hàng bổ sung", extra_options,

                                    max_selections=min(3, len(extra_options)),

                                    key="bc_extra")

selected = [st.session_state["bc_first"], st.session_state["bc_second"]] + [

    b for b in selected_extra if b in extra_options

]



view = ranking[ranking["bank"].isin(selected)].copy()



score_view = scores[scores["bank"].isin(selected)].copy()



max_row = view.loc[view["BDTI"].idxmax()]



min_row = view.loc[view["BDTI"].idxmin()]



gap = float(max_row["BDTI"] - min_row["BDTI"])



c1,c2,c3 = st.columns(3)



with c1:



    st.markdown(f'<div class="hm-bc-kpi yellow"><div class="label">🏆 Số ngân hàng so sánh</div><div class="number">{len(view)}</div><div class="detail">Tối đa 5 ngân hàng</div></div>', unsafe_allow_html=True)



with c2:



    st.markdown(f'<div class="hm-bc-kpi blue"><div class="label">📊 BDTI cao nhất</div><div class="number">{float(max_row["BDTI"]):.3f}</div><div class="detail">{html.escape(str(max_row["bank"]))}</div></div>', unsafe_allow_html=True)



with c3:



    st.markdown(f'<div class="hm-bc-kpi green"><div class="label">🌱 Chênh lệch BDTI</div><div class="number">{gap:.3f}</div><div class="detail">{html.escape(str(max_row["bank"]))} so với {html.escape(str(min_row["bank"]))}</div></div>', unsafe_allow_html=True)



plot_config={"displaylogo":False,"responsive":True}



layout=dict(template="plotly_white",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Arial",color="#36536a",size=12),margin=dict(l=25,r=22,t=26,b=30),legend_title_text="Ngân hàng")



left,right=st.columns(2)



with left:



    st.markdown('<div class="hm-bc-section">So sánh BDTI</div>',unsafe_allow_html=True)



    fig=px.bar(view.sort_values("BDTI"),x="BDTI",y="bank",orientation="h",color="bank",text="BDTI",color_discrete_map=COLORS)



    fig.update_traces(texttemplate="%{text:.3f}",textposition="outside",cliponaxis=False)



    fig.update_layout(**layout,height=315,showlegend=False,xaxis=dict(range=[0,110],title="Điểm BDTI"),yaxis_title="")



    st.plotly_chart(fig, width="stretch", config=plot_config)



with right:



    st.markdown('<div class="hm-bc-section">So sánh 4 trụ cột</div>',unsafe_allow_html=True)



    melted=view.melt(id_vars="bank",value_vars=list(PILLARS),var_name="Trụ cột",value_name="Điểm")



    fig=px.bar(melted,x="Trụ cột",y="Điểm",color="bank",barmode="group",text="Điểm",color_discrete_map=COLORS)



    fig.update_traces(texttemplate="%{text:.1f}",textposition="outside",cliponaxis=False)



    fig.update_layout(**layout,height=315,yaxis=dict(range=[0,115]),legend=dict(orientation="h",y=1.16,x=0))



    st.plotly_chart(fig, width="stretch", config=plot_config)



left,right=st.columns([1,1.3])



with left:



    st.markdown('<div class="hm-bc-section">Biểu đồ mạng nhện 4 trụ cột</div>',unsafe_allow_html=True)



    fig=go.Figure()



    for _,r in view.iterrows():



        b=str(r["bank"]); vals=[float(r[p]) for p in PILLARS]



        fig.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=list(PILLARS)+["A"],fill="toself",name=b,line=dict(color=COLORS.get(b,"#3f9b90")),opacity=.7))



    fig.update_layout(**layout,height=325,polar=dict(radialaxis=dict(range=[0,100],visible=True)),legend=dict(orientation="h",y=-.12))



    st.plotly_chart(fig, width="stretch", config=plot_config)



with right:



    st.markdown('<div class="hm-bc-section">Bản đồ nhiệt 16 tiêu chí</div>',unsafe_allow_html=True)



    criteria=[f"{p}{i}" for p in "ABCD" for i in range(1,5)]



    pivot=score_view.pivot_table(index="bank",columns="criterion",values="final_score",aggfunc="mean").reindex(index=selected,columns=criteria)



    z=pivot.to_numpy(dtype=float)



    fig=go.Figure(go.Heatmap(z=z,x=criteria,y=selected,zmin=0,zmax=2,colorscale=[[0,"#fffaf0"],[.5,"#ffe99a"],[1,"#399d66"]],colorbar=dict(title="Điểm"),hovertemplate="Ngân hàng: %{y}<br>Tiêu chí: %{x}<br>Điểm: %{z}<extra></extra>"))



    for i,b in enumerate(selected):



        for j,crit in enumerate(criteria):



            v=z[i,j]



            if np.isfinite(v):



                fig.add_annotation(x=crit,y=b,text=f"{v:g}",showarrow=False,font=dict(size=10,color="#133d33" if v<1.6 else "white"))



    fig.update_layout(**layout,height=325,xaxis_title="Tiêu chí",yaxis_title="",yaxis_autorange="reversed")



    st.plotly_chart(fig, width="stretch", config=plot_config)



def styled_comparison_table(frame: pd.DataFrame, *, numeric_columns=(), bank_column=None):

    """Render a safe, responsive table with an actual colored HTML header."""

    headings = "".join(f"<th scope=\"col\">{html.escape(str(c))}</th>" for c in frame.columns)

    body = []

    for _, record in frame.iterrows():

        cells = []

        for col in frame.columns:

            value = record[col]

            if pd.isna(value):

                shown = "—"

            elif col in numeric_columns:

                shown = f"{float(value):.3f}" if col != "Chênh lệch điểm" else f"{float(value):.2f}"

            elif col == "Hạng":

                shown = str(int(value))

            else:

                shown = str(value)

            css_class = "hm-num" if col in numeric_columns or col == "Hạng" else ("hm-bank" if col == bank_column else "")

            cells.append(f'<td class="{css_class}">{html.escape(shown)}</td>')

        body.append("<tr>" + "".join(cells) + "</tr>")

    st.markdown(

        '<div class="hm-bc-table-wrap"><table class="hm-bc-table">'

        f'<thead><tr>{headings}</tr></thead><tbody>{"".join(body)}</tbody>'

        '</table></div>',

        unsafe_allow_html=True,

    )





st.markdown('<div class="hm-bc-section">Bảng điểm tổng hợp</div>', unsafe_allow_html=True)

summary = view[["rank", "bank", "BDTI", "A", "B", "C", "D"]].rename(columns={

    "rank": "Hạng", "bank": "Ngân hàng", "A": "Trụ cột A",

    "B": "Trụ cột B", "C": "Trụ cột C", "D": "Trụ cột D",

})

styled_comparison_table(

    summary,

    numeric_columns={"BDTI", "Trụ cột A", "Trụ cột B", "Trụ cột C", "Trụ cột D"},

    bank_column="Ngân hàng",

)



st.markdown('<div class="hm-bc-section">Tiêu chí chênh lệch lớn nhất</div>', unsafe_allow_html=True)

spread = pivot.max(axis=0) - pivot.min(axis=0)

diff = spread.dropna().sort_values(ascending=False).reset_index()

diff.columns = ["Tiêu chí", "Chênh lệch điểm"]

styled_comparison_table(diff, numeric_columns={"Chênh lệch điểm"})



st.caption("Nguồn: ranking.csv và processed_scores.csv. Điểm chấm tự động cần được rà soát trước khi sử dụng làm kết luận chính thức.")
