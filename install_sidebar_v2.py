"""Run from project root. Creates backups, modifies only Python pages and shared sidebar."""
from pathlib import Path
import shutil, re, ast

ROOT=Path.cwd()
if not (ROOT/'app.py').is_file() or not (ROOT/'pages').is_dir():
    raise SystemExit('ERROR: Run this command inside the BANK-DX-RANK-2025 folder containing app.py and pages/.')
source=Path(__file__).resolve().with_name('hermetrics_sidebar.py')
if not source.is_file():
    raise SystemExit('ERROR: Place hermetrics_sidebar.py next to install_sidebar_v2.py.')
module=ROOT/'hermetrics_sidebar.py'
if module.exists():
    shutil.copy2(module, ROOT/'hermetrics_sidebar.py.before_v2.bak')
if source.resolve() != module.resolve():
    shutil.copy2(source, module)
else:
    print('Sidebar module da o dung vi tri')
files=[ROOT/'app.py', *sorted((ROOT/'pages').glob('*.py'))]
for path in files:
    original=path.read_text(encoding='utf-8-sig')
    if '# HERMETRICS_SIDEBAR_V2' in original:
        print('SKIP already installed:',path.name)
        continue
    raw=original
    # Remove the exact previously generated V1 injection, if present.
    raw=re.sub(r'\n# HERMETRICS_SHARED_SIDEBAR_V1\nfrom pathlib import Path as _HerMetricsPath\nfrom hermetrics_sidebar import apply_sidebar as _hermetrics_apply_sidebar\n_hermetrics_apply_sidebar\([^\n]*\)\n', '\n', raw)
    # Remove the previously generated Ranking-only menu; preserve its hero, graphs and data.
    if path.name=='2_Ranking_Dashboard.py':
        begin='# One consistent HerMetrics menu; hide Streamlit\'s filename-based navigation.'
        end='# The hero uses a separate image column: text cannot cover the buffalo cart.'
        if begin in raw and end in raw:
            a=raw.index(begin); b=raw.index(end,a)
            raw=raw[:a]+raw[b:]
        else:
            begin='# Sidebar navigation stays native'
            if begin in raw and end in raw:
                a=raw.index(begin);b=raw.index(end,a)
                raw=raw[:a]+raw[b:]
    # Evidence Explorer already contains its own matching navigation and evidence filters.
    # Preserve it, only add global style. Other pages with existing custom links are also preserved.
    existing_nav=bool(re.search(r'\bst\.page_link\s*\(',raw))
    tree=ast.parse(raw)
    config=next((n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='st' and n.func.attr=='set_page_config'),None)
    if config:
        lineno=config.end_lineno
    else:
        # Insert after top-level imports, never before future imports.
        imports=[n.end_lineno for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]
        lineno=max(imports,default=0)
    lines=raw.splitlines(keepends=True)
    insert='\n# HERMETRICS_SIDEBAR_V2\nfrom pathlib import Path as _HMPath\nfrom hermetrics_sidebar import render as _hm_render\n_hm_render(_HMPath(__file__).resolve().parent'+('.parent' if path.parent.name=='pages' else '')+', show_nav='+str(not existing_nav)+')\n\n'
    updated=''.join(lines[:lineno])+insert+''.join(lines[lineno:])
    compile(updated,str(path),'exec')
    backup=path.with_name(path.name+'.before_v2.bak')
    if not backup.exists():shutil.copy2(path,backup)
    path.write_text(updated,encoding='utf-8')
    print('UPDATED:',path.relative_to(ROOT),'existing custom nav:',existing_nav)
print('DONE. Restart Streamlit and refresh the browser.')

