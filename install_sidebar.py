"""Run from project root: python install_sidebar.py. Makes backups; no page content removed."""
from pathlib import Path
import shutil
import re
import ast

root = Path(__file__).resolve().parent
module = root / 'hermetrics_sidebar.py'
if not module.is_file():
    raise SystemExit('Missing hermetrics_sidebar.py next to installer.')
files = [root / 'app.py', *sorted((root / 'pages').glob('*.py'))]
files = [p for p in files if p.is_file()]
if not files:
    raise SystemExit('No app.py or pages/*.py found. Copy both installer files to project root.')
for file in files:
    raw = file.read_text(encoding='utf-8-sig')
    if 'HERMETRICS_SHARED_SIDEBAR_V1' in raw:
        print('ALREADY INSTALLED:', file.relative_to(root))
        continue
    is_evidence = 'Evidence_Explorer' in file.name
    # Remove only the redundant sidebar block from the previously supplied Ranking page.
    if file.name == '2_Ranking_Dashboard.py' and '# Sidebar navigation stays native' in raw and '# The hero uses a separate image column' in raw:
        start = raw.index('# Sidebar navigation stays native')
        end = raw.index('# The hero uses a separate image column', start)
        raw = raw[:start] + raw[end:]
    # Place after page config if present. Otherwise after initial imports, preserving future imports.
    lines = raw.splitlines(keepends=True)
    at = None
    for i, line in enumerate(lines):
        if re.match(r'^\s*st\.set_page_config\s*\(', line):
            # Only supports a single-line page config; do not risk breaking a multiline call.
            if ')' not in line:
                raise SystemExit(f'Multiline set_page_config in {file}; please send file for manual patch.')
            at = i + 1
            break
    if at is None:
        tree = ast.parse(raw)
        imports = [node.end_lineno for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
        at = max(imports) if imports else 0
    snippet = ('\n# HERMETRICS_SHARED_SIDEBAR_V1\n'
               'from pathlib import Path as _HerMetricsPath\n'
               'from hermetrics_sidebar import apply_sidebar as _hermetrics_apply_sidebar\n'
               '_hermetrics_apply_sidebar(_HerMetricsPath(__file__).resolve().parent'
               + ('.parent' if file.parent.name == 'pages' else '')
               + f', existing_custom_nav={is_evidence})\n\n')
    changed = ''.join(lines[:at]) + snippet + ''.join(lines[at:])
    try:
        compile(changed, str(file), 'exec')
    except SyntaxError as exc:
        raise SystemExit(f'Cannot patch {file.name}: {exc}')
    backup = file.with_name(file.name + '.before_sidebar.bak')
    if not backup.exists():
        shutil.copy2(file, backup)
    file.write_text(changed, encoding='utf-8')
    print('UPDATED:', file.relative_to(root), 'BACKUP:', backup.name)
print('Done. Restart Streamlit and hard-refresh browser.')
