from pathlib import Path
import shutil, re, ast

root = Path(__file__).resolve().parent
ranking = root / 'pages' / '2_Ranking_Dashboard.py'
sidebar = root / 'hermetrics_sidebar.py'
assets = root / 'assets' / 'vietnam_art'
assets.mkdir(parents=True, exist_ok=True)
for name in ('ranking_left_art.png', 'ranking_right_bamboo.png'):
    source = root / 'assets' / 'vietnam_art' / name
    if not source.is_file():
        raise FileNotFoundError(f'Missing artwork: {source}')
if not ranking.is_file() or not sidebar.is_file():
    raise FileNotFoundError('Run installer from project root alongside app.py, hermetrics_sidebar.py and pages/')

text = ranking.read_text(encoding='utf-8-sig')
marker = 'from ranking_side_art import render_ranking_side_art'
if marker not in text:
    lines = text.splitlines(keepends=True)
    idx = next((i for i, line in enumerate(lines) if re.match(r'^st\.set_page_config\(', line)), None)
    if idx is None:
        raise ValueError('Could not find st.set_page_config in Ranking page')
    lines.insert(idx + 1, '\n# Decorative Vietnamese art (Ranking page only)\nfrom ranking_side_art import render_ranking_side_art\nrender_ranking_side_art()\n')
    candidate = ''.join(lines)
    ast.parse(candidate)
    shutil.copy2(ranking, ranking.with_suffix('.py.before_art.bak'))
    ranking.write_text(candidate, encoding='utf-8')
    print('UPDATED Ranking page')
else:
    print('Ranking art already installed')

# Add sidebar artwork to shared sidebar, keeping its existing navigation intact.
text = sidebar.read_text(encoding='utf-8-sig')
marker = '# HERMETRICS_SIDEBAR_ART_V3'
if marker not in text:
    patch = '''\n\n# HERMETRICS_SIDEBAR_ART_V3\ndef _hm_add_sidebar_art():\n    from pathlib import Path\n    import streamlit as st\n    art = Path(__file__).resolve().parent / "assets" / "vietnam_art" / "lang_que_viet_nam.png"\n    if art.is_file():\n        with st.sidebar:\n            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)\n            st.image(str(art), use_container_width=True)\n\n_hm_previous_apply_sidebar = globals().get("apply_sidebar")\nif _hm_previous_apply_sidebar is not None:\n    def apply_sidebar(*args, **kwargs):\n        result = _hm_previous_apply_sidebar(*args, **kwargs)\n        if not kwargs.get("existing_custom_nav", False):\n            _hm_add_sidebar_art()\n        return result\n\n_hm_previous_render = globals().get("render")\nif _hm_previous_render is not None:\n    def render(*args, **kwargs):\n        result = _hm_previous_render(*args, **kwargs)\n        if kwargs.get("show_nav", True) and not kwargs.get("existing_custom_nav", False):\n            _hm_add_sidebar_art()\n        return result\n'''
    candidate = text + patch
    ast.parse(candidate)
    shutil.copy2(sidebar, sidebar.with_suffix('.py.before_art.bak'))
    sidebar.write_text(candidate, encoding='utf-8')
    print('UPDATED shared sidebar artwork')
else:
    print('Shared sidebar artwork already installed')
print('DONE. Restart Streamlit and hard-refresh the browser.')
