#!/usr/bin/env python3
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
COMPANIONS={
    'money-trail':'money_trail.py',
    'performance-truth':'performance_readiness.py',
    'basis-proof':'basis_proof.py',
    'ledger-repair':'ledger_delta.py',
    'model-sanity':'model_sanity.py',
    'close-the-books':'close_books.py',
}
for skill,tool in COMPANIONS.items():
    dst=ROOT/'skills'/'financial-truth'/skill/'scripts'
    dst.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'tools'/tool,dst/tool)
    shutil.copy2(ROOT/'tools'/'common.py',dst/'common.py')
print(f'built {len(COMPANIONS)} deterministic skill companions')
