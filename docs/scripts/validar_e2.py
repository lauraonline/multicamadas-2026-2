"""Valida artefatos documentais; não executa testes do sistema de negócio."""
from pathlib import Path
import re, json, xml.etree.ElementTree as ET
import pymupdf
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'docs'
errors=[]; links=0
for f in [ROOT/'README.md',*D.rglob('*.md')]:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
  if re.match(r'https?://',target):continue
  path=target.split('#')[0]
  if path and not (f.parent/path).exists():errors.append(f'{f.relative_to(ROOT)}: link ausente {target}')
  links+=1
expected={f'RF{i:02}' for i in range(1,14)}|{f'RN{i:02}' for i in range(1,8)}|{f'RNF{i:02}' for i in range(1,8)}|{'RF-E01','RN-E01','RN-E02','RNF-E01','RNF-E02'}
rows=re.findall(r'^\| ((?:RF|RNF|RN)(?:-E)?\d{2}) \|',(D/'rastreabilidade.md').read_text(),re.M)
if set(rows)!=expected or len(rows)!=32:errors.append('Matriz sem cobertura única dos 32 IDs')
adrs=sorted((D/'adr').glob('adr-*.md'))
if len(adrs)!=6:errors.append('Esperados seis ADRs')
for f in adrs:
 s=f.read_text()
 for heading in ['Contexto','Decisão','Alternativas consideradas','Trade-offs e custo/benefício','Verificação e revisão','Rastreabilidade']:
  if '## '+heading not in s:errors.append(f'{f.name}: seção {heading} ausente')
graphs=json.loads((D/'diagramas/modelos.json').read_text());xml=ET.parse(D/'arquitetura.drawio').getroot()
if len(xml.findall('diagram'))!=4:errors.append('Esperadas quatro abas editáveis')
for g in graphs:
 ids={n['id'] for n in g['nodes']}
 for e in g['edges']:
  if e['a'] not in ids or e['b'] not in ids:errors.append(f"Aresta inválida em {g['name']}")
 if not (D/'diagramas'/f"{g['name']}.png").exists():errors.append('PNG ausente')
pdf=pymupdf.open(D/'SaudeCerta_E2_Projeto_Arquitetural_Core4Tech.pdf');text='\n'.join(p.get_text() for p in pdf)
for marker in [*expected,*[f'ADR-{i:03}' for i in range(1,7)],*[f'CQ{i:02}' for i in range(1,10)]]:
 if marker not in text:errors.append(f'PDF sem {marker}')
if '\x00' in text or '\ufffd' in text:errors.append('PDF com glifo ausente')
for i,page in enumerate(pdf):
 for word in page.get_text('words'):
  x0,y0,x1,y1=word[:4]
  if x0<25 or x1>page.rect.width-25 or y0<15 or y1>page.rect.height-15:errors.append(f'Texto fora da margem da página {i+1}: {word[4]}')
if errors:raise SystemExit('\n'.join(errors))
print(f'OK: {links} links locais, 32 requisitos/regras, 6 ADRs, 4 diagramas, PDF de {len(pdf)} páginas; IDs e margens textuais válidos.')
