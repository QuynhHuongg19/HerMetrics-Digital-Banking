from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
page = root / 'pages' / '3_Bank_Profile.py'
if not page.is_file():
    raise SystemExit('ERROR: Place this script beside app.py, inside BANK-DX-RANK-2025.')
source = page.read_text(encoding='utf-8-sig')
marker = '# HERMETRICS_BANK_SELECTOR_2026'
if marker in source:
    print('Selector already installed. No changes made.')
    raise SystemExit(0)
old = '''banks = ranking.sort_values("rank")["bank"].tolist()
bank = st.selectbox("Chọn ngân hàng cần phân tích", banks)'''
# tolerate spacing and empty lines
import re
pattern = r'banks\s*=\s*ranking\.sort_values\([\'\"]rank[\'\"]\)\[[\'\"]bank[\'\"]\]\.tolist\(\)\s*\nbank\s*=\s*st\.selectbox\(\s*[\'\"]Chọn ngân hàng cần phân tích[\'\"]\s*,\s*banks\s*\)'
if not re.search(pattern, source):
    raise SystemExit('ERROR: Could not find the original bank selector. No changes made.')
replacement = '''# HERMETRICS_BANK_SELECTOR_2026
st.markdown("""
<style>
.st-key-hm_bank_selector_2026 {
    position: relative; isolation: isolate; overflow: hidden;
    padding: 24px 28px 26px; border-radius: 18px;
    border: 1px solid #ead5e5;
    background: linear-gradient(110deg, #fffaf8 0%, #fff3f7 54%, #eaf2ff 100%);
    box-shadow: 0 5px 20px rgba(98, 46, 88, .06);
}
.st-key-hm_bank_selector_2026::before,
.st-key-hm_bank_selector_2026::after {
    content: ""; position: absolute; pointer-events: none; z-index: -1;
    right: 0; bottom: 60px; width: 55%; height: 65%;
    background-repeat: no-repeat; background-size: 100% 100%;
}
.st-key-hm_bank_selector_2026::before {
    background: #e1d9f6;
    clip-path: polygon(0 100%, 16% 80%, 28% 91%, 45% 42%, 56% 68%, 73% 20%, 86% 49%, 100% 12%, 100% 100%);
    opacity: .52;
}
.st-key-hm_bank_selector_2026::after {
    height: 42%; width: 47%; background: #f3c9df;
    clip-path: polygon(0 100%, 17% 74%, 30% 90%, 48% 30%, 61% 65%, 79% 15%, 91% 48%, 100% 23%, 100% 100%);
    opacity: .62;
}
.hm-bank-select-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(28px, 3vw, 45px); font-weight: 800;
    line-height: 1.2; color: #851943; margin: 0 0 7px;
}
.hm-bank-select-description {font-size: 14px; color: #72596b; margin-bottom: 17px;}
.st-key-hm_bank_selector_2026 [data-baseweb="select"] > div {
    min-height: 72px !important; background: rgba(255,255,255,.96) !important;
    border: 2px solid #e8a8c7 !important; border-radius: 13px !important;
}
.st-key-hm_bank_selector_2026 [data-baseweb="select"] span {
    font-size: clamp(23px, 2.5vw, 35px) !important;
    font-weight: 800 !important; color: #851943 !important;
}
@media(max-width:720px){
 .st-key-hm_bank_selector_2026{padding:18px 15px 20px;}
 .st-key-hm_bank_selector_2026 [data-baseweb="select"] > div{min-height:62px!important;}
}
</style>
""", unsafe_allow_html=True)

banks = ranking.sort_values("rank")["bank"].tolist()
with st.container(key="hm_bank_selector_2026"):
    st.markdown(
        '<div class="hm-bank-select-heading">🏦 Chọn ngân hàng cần phân tích</div>'
        '<div class="hm-bank-select-description">Lựa chọn ngân hàng để khám phá kết quả chuyển đổi số và các chỉ số đánh giá</div>',
        unsafe_allow_html=True,
    )
    bank = st.selectbox(
        "Chọn ngân hàng cần phân tích",
        banks,
        label_visibility="collapsed",
        key="hm_bank_choice_2026",
    )'''
updated = re.sub(pattern, lambda _: replacement, source, count=1)
compile(updated, str(page), 'exec')
backup = page.with_suffix('.py.before_selector_2026.bak')
shutil.copy2(page, backup)
page.write_text(updated, encoding='utf-8')
print('SUCCESS: Updated', page)
print('BACKUP:', backup)
