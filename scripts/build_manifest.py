#!/usr/bin/env python3
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
VERSION=(ROOT/'VERSION').read_text(encoding='utf-8').strip()

def section(text, heading):
    m=re.search(rf'^## {re.escape(heading)}\n\n(.+?)(?=\n## |\Z)', text, re.M|re.S)
    if not m: return None
    return ' '.join(m.group(1).strip().split())

items=[]
for skill in sorted((ROOT/'skills').glob('*/*/SKILL.md')):
    text=skill.read_text(encoding='utf-8')
    name=re.search(r'^name:\s*(.+)$', text, re.M).group(1).strip()
    desc=re.search(r'^description:\s*(.+)$', text, re.M).group(1).strip()
    items.append({
        'name':name,
        'family':skill.parents[1].name,
        'path':str(skill.relative_to(ROOT)),
        'description':desc,
        'rule':section(text,'Rule'),
        'falsify':section(text,'Falsify it'),
        'deterministic_companion': (skill.parent/'scripts').exists(),
    })
adapters=sorted(p.name for p in (ROOT/'adapters').iterdir() if p.is_dir() and not p.name.startswith('.'))
manifest={
    'schema':'dale-os/manifest/v1',
    'version':VERSION,
    'entrypoints':{'agent':'AGENTS.md','human':'README.md','llm_index':'llms.txt','challenge':'CHALLENGE.md'},
    'trust':{'financial_mutation':False,'canonical_skill_root':'skills/','generated_adapters':['eve']},
    'skills':items,
    'deterministic_tools':sorted(p.name for p in (ROOT/'tools').glob('*.py') if p.name!='common.py'),
    'adapters':adapters
}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+"\n",encoding='utf-8')
print(f"manifest: {len(items)} skills, {len(adapters)} adapters, version {VERSION}")
