"""Gera o pacote E2 localmente: diagramas drawio/PNG e PDF consolidado."""
from pathlib import Path
import io, json, math, re, html, xml.etree.ElementTree as ET
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
import pymupdf
ROOT=Path(__file__).resolve().parents[2]; DOCS=ROOT/'docs'
FONT=Path(reportlab.__file__).parent/'fonts'
for name,file in [('Body','Vera.ttf'),('BodyBold','VeraBd.ttf'),('BodyItalic','VeraIt.ttf')]: pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
NAVY=colors.HexColor('#14344a'); TEAL=colors.HexColor('#087e8b'); GRAY=colors.HexColor('#526675')
def draw_graph(g):
 buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(g['w'],g['h']))
 def rect(x,y,w,h): return x,g['h']-y-h,w,h
 def text(x,y,t,size=20,color=NAVY):
  c.setFillColor(color); c.setFont('Body',size); c.drawCentredString(x,g['h']-y,t)
 c.setFillColor(colors.white);c.rect(0,0,g['w'],g['h'],fill=1,stroke=0)
 text(g['w']/2,32,g['title'],26)
 if g['boundary']:
  x,y,w,h,t=g['boundary']; c.setStrokeColor(TEAL);c.setDash(7,5);c.roundRect(*rect(x,y,w,h),12,fill=0);c.setDash();text(x+w/2,y+25,t,20)
 nodes={n['id']:n for n in g['nodes']}
 def anchor(n,other):
  x=n['x']+n['w']/2;y=n['y']+n['h']/2;dx=other['x']+other['w']/2-x;dy=other['y']+other['h']/2-y
  t=min(n['w']/2/abs(dx) if dx else 1e9,n['h']/2/abs(dy) if dy else 1e9)
  return x+t*dx,y+t*dy
 for idx,e in enumerate(g['edges']):
  a=nodes[e['a']];b=nodes[e['b']];x1,y1=anchor(a,b);x2,y2=anchor(b,a)
  # Parallel opposite relations are rendered as a single bidirectional line.
  reverse=next((z for z in g['edges'][:idx] if z['a']==e['b'] and z['b']==e['a']),None)
  if reverse: continue
  rev=next((z for z in g['edges'][idx+1:] if z['a']==e['b'] and z['b']==e['a']),None)
  c.setStrokeColor(GRAY);c.setLineWidth(2);c.line(x1,g['h']-y1,x2,g['h']-y2)
  def arrow(x,y,xx,yy):
   ang=math.atan2(y-yy,x-xx);p=c.beginPath();p.moveTo(x,g['h']-y)
   for d in [-.42,.42]:p.lineTo(x-12*math.cos(ang+d),g['h']-(y-12*math.sin(ang+d)))
   p.close();c.setFillColor(GRAY);c.drawPath(p,fill=1,stroke=0)
  arrow(x2,y2,x1,y1)
  if rev: arrow(x1,y1,x2,y2)
  label=e['label']+(' / '+rev['label'] if rev else '')
  mx=(x1+x2)/2;my=(y1+y2)/2
  size=17;tw=pdfmetrics.stringWidth(label,'Body',size)
  c.setFillColor(colors.white);c.rect(mx-tw/2-4,g['h']-my-4,tw+8,23,fill=1,stroke=0);text(mx,my,label,size)
 for n in g['nodes']:
  kind=n.get('kind');fill={'system':'#e0f2f4','external':'#edf0f3','data':'#e9f3e9','person':'#e5edf8'}.get(kind,'#f1f7fa')
  c.setFillColor(colors.HexColor(fill));c.setStrokeColor(TEAL if kind=='system' else GRAY);c.roundRect(*rect(n['x'],n['y'],n['w'],n['h']),10,fill=1,stroke=1)
  lines=n['label'].split('\n');start=n['y']+n['h']/2-(len(lines)-1)*13+6
  for j,line in enumerate(lines):text(n['x']+n['w']/2,start+j*26,line,20 if j==0 else 18)
 text(g['w']/2,g['h']-12,'Setas indicam direção da interação; multiplicidades no domínio: origem : destino.',16)
 c.save();pdf=pymupdf.open(stream=buf.getvalue(),filetype='pdf');pix=pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5));pix.save(str(DOCS/'diagramas'/f"{g['name']}.png"));pdf.close()

def drawio(graphs):
 root=ET.Element('mxfile',host='app.diagrams.net',type='device')
 for g in graphs:
  dia=ET.SubElement(root,'diagram',id=g['name'],name=g['title']);model=ET.SubElement(dia,'mxGraphModel',page='1',pageWidth=str(g['w']),pageHeight=str(g['h']));r=ET.SubElement(model,'root');ET.SubElement(r,'mxCell',id='0');ET.SubElement(r,'mxCell',id='1',parent='0')
  if g['boundary']:
   x,y,w,h,t=g['boundary'];cell=ET.SubElement(r,'mxCell',id='boundary',value=t,style='rounded=1;dashed=1;fillColor=none;verticalAlign=top;fontSize=20;',vertex='1',parent='1');ET.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
  for n in g['nodes']:
   cell=ET.SubElement(r,'mxCell',id=n['id'],value=n['label'],style='rounded=1;whiteSpace=wrap;html=0;fontSize=20;fillColor=#f1f7fa;strokeColor=#087e8b;',vertex='1',parent='1');ET.SubElement(cell,'mxGeometry',x=str(n['x']),y=str(n['y']),width=str(n['w']),height=str(n['h']),attrib={'as':'geometry'})
  for i,e in enumerate(g['edges']):
   cell=ET.SubElement(r,'mxCell',id=f'edge{i}',value=e['label'],style='edgeStyle=none;endArrow=block;fontSize=17;labelBackgroundColor=#ffffff;',edge='1',source=e['a'],target=e['b'],parent='1');ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
 ET.indent(root);ET.ElementTree(root).write(DOCS/'arquitetura.drawio',encoding='utf-8',xml_declaration=True)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontName='Body',fontSize=9,leading=13,spaceAfter=7,textColor=NAVY))
styles.add(ParagraphStyle(name='SmallCell',fontName='Body',fontSize=7.4,leading=10,spaceAfter=2,textColor=NAVY))
for key,size,lead in [('Heading1',22,27),('Heading2',14,19),('Heading3',11,15)]:styles[key].fontName='BodyBold';styles[key].fontSize=size;styles[key].leading=lead;styles[key].textColor=TEAL;styles[key].spaceBefore=12;styles[key].spaceAfter=10;styles[key].keepWithNext=True
styles['Title'].fontName='BodyBold';styles['Title'].textColor=NAVY

def inline(s):
 s=html.escape(s.replace('—','-').replace('–','-').replace('↔','<->').replace('→','->'))
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'<font color="#087e8b">\1</font>',s)
 return s

def parse(md):
 story=[];lines=md.splitlines();i=0
 while i<len(lines):
  l=lines[i].strip()
  if not l:i+=1;continue
  if l.startswith('!['):
   path=re.search(r'\]\(([^)]+)\)',l).group(1);img=Image(str(DOCS/path));ratio=min(480/img.imageWidth,600/img.imageHeight);img.drawWidth=img.imageWidth*ratio;img.drawHeight=img.imageHeight*ratio;story.append(img);story.append(Spacer(1,10));i+=1;continue
  if l.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch('[: -]+',c) for c in cells):rows.append([Paragraph(inline(c),styles['SmallCell']) for c in cells])
    i+=1
   count=len(rows[0]);widths={3:[105,175,200],4:[68,125,85,202]}.get(count,[480/count]*count)
   table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dceef0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),1,TEAL)]));story.extend([table,Spacer(1,12)]);continue
  if l.startswith('#'):
   level=len(l)-len(l.lstrip('#'));story.append(Paragraph(inline(l.lstrip('# ')),styles[f'Heading{min(level,3)}']));i+=1;continue
  para=[l];i+=1
  while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![','- ')) and not re.match(r'^\d+\. ',lines[i]):para.append(lines[i].strip());i+=1
  txt=' '.join(para)
  if txt.startswith('- '):txt='• '+txt[2:]
  story.append(Paragraph(inline(txt),styles['Text']))
 return story

def footer(c,doc):
 c.saveState();w,h=A4;c.setStrokeColor(TEAL);c.line(55,h-39,w-55,h-39);c.setFont('Body',8);c.setFillColor(GRAY);c.drawString(55,h-30,'SAÚDECERTA / E2 - Projeto arquitetural');c.drawString(55,30,'Core4 Tech | IFPA | C795NL | 2026.2');c.drawRightString(w-55,30,str(doc.page));c.restoreState()

def main():
 graphs=json.loads((DOCS/'diagramas/modelos.json').read_text())
 drawio(graphs)
 for g in graphs:draw_graph(g)
 story=[Spacer(1,65),Paragraph('SaúdeCerta',styles['Title']),Spacer(1,24),Paragraph('Projeto arquitetural',styles['Heading1']),Paragraph('ENTREGA E2 • 04/11/2026',styles['Heading2']),Spacer(1,25),Paragraph('Core4 Tech',styles['Heading2']),Paragraph('Laura Alves<br/>Gabriel Prado Brandão<br/>Adinayane Souza<br/>Ruan William Leão',styles['Text']),Spacer(1,20),Paragraph('Instituto Federal do Pará - Campus Belém<br/>Tecnologia em Análise e Desenvolvimento de Sistemas<br/>Desenvolvimento de Aplicações Multicamadas - TEADS0347<br/>Turma C795NL - Período 2026.2<br/>Docente: Márcio Goes do Nascimento',styles['Text']),Spacer(1,18),Paragraph('Arquitetura alvo para revisão da equipe. As verificações de negócio e qualidade estão planejadas para E3/PF.',styles['Text']),PageBreak()]
 story+=parse('# Roteiro de leitura\n\n1. Arquitetura: C4, camadas, contratos, fluxos e operação.\n2. Modelo de domínio: entidades, relações e invariantes.\n3. Cenários CQ01-CQ09: medidas e protocolos de validação.\n4. ADR-001 a ADR-006: alternativas e custo/benefício.\n5. Matriz: requisitos, arquitetura e verificações.\n6. Referências e encaminhamento da entrega.\n\nO documento consolida integralmente os Markdown da E2. A E1 original e seu catálogo permanecem no mesmo repositório. IDs oficiais e complementares são distinguidos; propostas e resultados de implementação não são confundidos.')
 files=['arquitetura.md','modelo-dominio.md','cenarios-qualidade.md']+[f'adr/adr-{i:03}.md' for i in range(1,7)]+['rastreabilidade.md','referencias.md']
 for file in files:story.append(PageBreak());story+=parse((DOCS/file).read_text(encoding='utf-8'))
 output=DOCS/'SaudeCerta_E2_Projeto_Arquitetural_Core4Tech.pdf'
 SimpleDocTemplate(str(output),pagesize=A4,rightMargin=55,leftMargin=55,topMargin=55,bottomMargin=50,title='SaúdeCerta - E2 Projeto Arquitetural',author='Core4 Tech').build(story,onFirstPage=footer,onLaterPages=footer)
 print(f'Gerado: {output}')
if __name__=='__main__':main()
