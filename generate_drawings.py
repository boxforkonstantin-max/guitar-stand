#!/usr/bin/env python3
"""R5: one geometry source for browser, PDF, SVG, DXF and OpenSCAD. mm."""
import json, math, hashlib
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
D=json.loads((ROOT/'design.json').read_text())
# Assembly placement is derived from support planes, not eyeballed offsets.
k=next(p for p in D['parts'] if p['id']=='K'); ang=math.radians(k['rotation'][0]); co,si=math.cos(ang),math.sin(ang)
D['equipment']['amp']['pos']=[295,251+208*co+4*si,230+208*si-4*co]
u=next(p for p in D['parts'] if p['id']=='U');u['pos']=[295,251+21.5*co+171*si,230+21.5*si-171*co]
D['equipment']['pedal']['pos']=[295,90+(45-210)*math.tan(math.radians(10))+31.5/math.cos(math.radians(10)),45]
W,H=D['sheet']['width'],D['sheet']['height']
T=D['thickness']
COL={'B':'#d4b78e','T':'#b8ced0','K':'#9ab6bd','A':'#e3c781','N':'#bda694','U':'#afc2aa'}
# Validated bounding-box nesting: all variants fit, no curve-dependent nesting.
PACK=[('B3','B',6,6,0),('B1','B',6,794,90),('B4','B',432,6,0),
 ('A2','A',794,794,0),('B2','B',858,6,0),('T2','T',1284,6,90),
 ('N2','N',1366,602,90),('N1','N',1462,602,90),('A1','A',1558,602,90),
 ('T1','T',1620,6,90),('K1','K',1956,6,90),('K2','K',1984,578,90),('U1','U',2350,6,90),('U2','U',2381,6,90)]

def rect(w,h): return [[0,0],[w,0],[w,h],[0,h]]
def area(p): return abs(sum(x*p[(i+1)%len(p)][1]-y*p[(i+1)%len(p)][0] for i,(x,y) in enumerate(p)))/2
def bbox(p): return [min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)]
def placed(p,x,y,r):
 a=math.radians(r); q=[[u*math.cos(a)-v*math.sin(a),u*math.sin(a)+v*math.cos(a)] for u,v in p]
 b=bbox(q); return [[round(u-b[0]+x,6),round(v-b[1]+y,6)] for u,v in q]
def profiles(kind):
 def f(t):
  if kind=='arc': return t*t
  if kind=='lean':
   e=.18; slope=1/(1-e)
   return slope*t*t/(2*e) if t<e else 1-slope*(1-t)**2/(2*e) if t>1-e else slope*(t-e/2)
  return t*t*(3-2*t)
 return [[round(90*f(i/160),6),D['sideHeight']*i/160] for i in range(161)]+[[420,D['sideHeight']],[420,0]]
def tabletop(w,h,r):
 p=[]
 for cx,cy,start in [(r,r,180),(w-r,r,270),(w-r,h-r,0),(r,h-r,90)]:
  p += [[round(cx+r*math.cos(math.radians(start+i*90/16)),6),round(cy+r*math.sin(math.radians(start+i*90/16)),6)] for i in range(17)]
 return p
def dxf(polys):
 s='0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1015\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n'
 for layer,p in polys:
  s+=f'0\nLWPOLYLINE\n100\nAcDbEntity\n8\n{layer}\n100\nAcDbPolyline\n90\n{len(p)}\n70\n1\n'
  for x,y in p: s+=f'10\n{x:.6f}\n20\n{y:.6f}\n'
 return s+'0\nENDSEC\n0\nEOF\n'
def svg(items):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white" stroke="#222"/>'
 for i in items:
  p=i['poly']; b=bbox(p); pts=' '.join(f'{x},{H-y}' for x,y in p)
  s+=f'<polygon data-id="{i["id"]}" points="{pts}" fill="{COL[i["code"]]}" stroke="#333" stroke-width="1"/><text x="{(b[0]+b[2])/2}" y="{H-(b[1]+b[3])/2}" text-anchor="middle" font-family="Arial" font-size="25">{i["id"]}</text>'
 return s+'</svg>'

pdfmetrics.registerFont(TTFont('UI','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
PW,PH=landscape(A3)
def text(c,x,y,s,size=10,bold=False):
 c.setFillColorRGB(.1,.14,.16); c.setFont('Bold' if bold else 'UI',size); c.drawString(x,y,s)
def poly(c,p,x,y,s,color='#d4b78e'):
 q=c.beginPath(); q.moveTo(x+p[0][0]*s,y+p[0][1]*s)
 for u,v in p[1:]: q.lineTo(x+u*s,y+v*s)
 q.close(); c.setFillColor(color); c.setStrokeColorRGB(.2,.25,.27); c.setLineWidth(.5); c.drawPath(q,stroke=1,fill=1)
def header(c,title,sub,n):
 text(c,35,PH-38,title,20,True); text(c,35,PH-58,sub,10)
 text(c,35,20,f'R6 • Горизонтальная полка Katana, не выпуск в производство • мм • лист {n}',8)
def dim(c,x,y,w,h):
 text(c,x,y-16,str(w),9); text(c,x+w*.55+10,y+h*.28,str(h),9)
def pdf(path,key,m):
 c=canvas.Canvas(str(path),pagesize=(PW,PH)); c.setTitle('Гитарная стойка R6 / '+key)
 header(c,'Раскрой двух стоек / '+D['profiles'][key]['name'],'Лист 2440 × 1220 × 18. Отступ 6; зазор между габаритами ≥6. Без зеркалирования.',1)
 s=.455; x=35; y=150
 poly(c,rect(W,H),x,y,s,'#ffffff')
 for i in m['layout']:
  poly(c,i['poly'],x,y,s,COL[i['code']]); b=bbox(i['poly']); text(c,x+(b[0]+b[2])/2*s-10,y+(b[1]+b[3])/2*s,i['id'],9,True)
 text(c,35,110,f'14 деталей с передними упорами; использование листа {m["verification"]["utilizationPercent"]}%. Один лист на два изделия.',12,True)
 text(c,35,87,'Это раскрой внешних контуров. Пазы, крепёж и отверстия для кабелей не включены в слой CUT.',10)
 text(c,35,66,'Зазор 6 мм требует согласования инструмента и стратегии CAM; припуск на чистовую обработку не заложен.',10)
 c.showPage()
 header(c,'Геометрия деталей и варианты дизайна','Все три варианта имеют одинаковые габариты и посадочные отметки. Толщина 18 мм.',2)
 for j,(k,pr) in enumerate(D['profiles'].items()):
  ox=40+j*240; oy=290; poly(c,profiles(pr['formula']),ox,oy,.5,COL['B']); text(c,ox,260,pr['name'],10,True)
  text(c,ox,242,'Низ 420 / верх 330 / высота 782',9)
 text(c,790,PH-110,'Ведомость на 2 изделия',14,True)
 yy=PH-150
 for code,p in m['polygons'].items():
  b=bbox(p); qty=4 if code=='B' else 2
  text(c,790,yy,f'{code}: {b[2]:g} × {b[3]:g} × 18   /   {qty} шт.',12); yy-=35
 text(c,790,yy-10,'T: скругление всех углов R24.',10)
 text(c,40,185,'Боковина 782 + столешница 18 = общая высота 800.',12,True)
 text(c,40,158,'Чистый пролёт 554 мм; детали K/A/N 566 мм рассчитаны на заход по 6 мм в боковины.',11)
 text(c,40,134,'Пазы и соединения требуют отдельной деталировки по фактической толщине фанеры с покрытием.',11)
 text(c,40,110,'Полилиния передней кромки: 160 сегментов. Координаты одинаковы в модели, SVG и DXF.',11)
 c.showPage()
 header(c,'Сборка / положение полок','Слева: вид спереди. Справа: вид сбоку, передняя кромка слева. Оборудование условное.',3)
 s=.67; ox=70; oy=160
 for x in [0,572]: poly(c,rect(18,782),ox+x*s,oy,s)
 for part in D['parts'][2:]:
  w,h=part['size']; px,py,pz=part['pos']; a=math.radians(part['rotation'][0]);
  hh=18 if part['plane']=='horizontal' else h
  if part['plane']=='horizontal' and a: hh=h*abs(math.sin(a))+18*math.cos(a)
  poly(c,rect(w,hh),ox+(px-w/2)*s,oy+(py-hh/2)*s,s,COL[part['code']])
 e=D['equipment']['amp']; ew,eh,ed=e['dims']; ex,ey,ez=e['pos']
 ea=math.radians(e['rotation'][0]);ehproj=eh*math.cos(ea)+ed*abs(math.sin(ea))
 poly(c,rect(ew,ehproj),ox+(ex-ew/2)*s,oy+(ey-ehproj/2)*s,s,'#6c7275')
 text(c,ox,115,'Ширина 590 / высота 800',12,True)
 sx=625; poly(c,m['polygons']['B'],sx,oy,s,'#ede5d8')
 for part in D['parts'][2:]:
  w,d=part['size']; px,py,pz=part['pos']; a=math.radians(part['rotation'][0]); hh,dd=(18,d) if part['plane']=='horizontal' else (d,18)
  pts=[]
  for z,y in [(-dd/2,-hh/2),(dd/2,-hh/2),(dd/2,hh/2),(-dd/2,hh/2)]: pts.append([pz+z*math.cos(a)+y*math.sin(a),py+y*math.cos(a)-z*math.sin(a)])
  poly(c,pts,sx,oy,s,COL[part['code']]); text(c,sx+300,oy+py*s+(16 if part['id']=='U' else 0),part['id'],10,True)
 ep=[[ez+zz*math.cos(ea)+yy*math.sin(ea),ey+yy*math.cos(ea)-zz*math.sin(ea)] for zz,yy in [(-ed/2,-eh/2),(ed/2,-eh/2),(ed/2,eh/2),(-ed/2,eh/2)]]
 poly(c,ep,sx,oy,s,'#6c7275')
 text(c,sx,115,'Глубины: A 420 → K 360 → T 330',12,True)
 text(c,40,75,'T верх 800; K горизонтальная, верх Y260; A центр Y90, наклон 10°; упор U 25 мм.',10)
 text(c,40,53,'Оси сборки: X ширина, Y высота, Z от передней кромки к задней. Координаты центров - в model.json.',10)
 c.showPage()
 header(c,'Кабели и ограничения проекта','Отверстия ниже - предложения, не обязательная обработка. Точные модели оборудования нужно подтвердить.',4)
 for j,proposal in enumerate(D['cableProposals']):
  code=proposal['part']; p=m['polygons'][code]; ox=40+j*375; oy=440; sc=.55
  poly(c,p,ox,oy,sc,COL[code]); u,v=proposal['center']; c.setStrokeColorRGB(.75,.3,.1); c.circle(ox+u*sc,oy+v*sc,proposal['diameter']/2*sc,stroke=1)
  text(c,ox,410,f'{code}: Ø40, центр {u} / {v}',12,True); text(c,ox,390,'От левого переднего угла, вид сверху.',9)
 notes=[
  'Клипсы на внутренней стороне правой боковины: задняя зона Z≈380 мм; окончательные места после примерки.',
  'Запас сигнального кабеля - на липучке под K. Не перекрывать задние отверстия усилителя.',
  'Сетевой кабель вести отдельно от аудиолинии; отверстия защитить втулками, не делать перегиб у штекера.',
  'Katana-50 MkII: AC IN, USB-B, AUX IN, FOOT CONTROL/EXP, PHONES/REC OUT, POWER AMP IN.',
  'AIRSTEP Kat Edition: USB-C → USB-B Katana. Разъёмы схематичны, координаты не обмерены.',
  'ВАЖНО: руководство BOSS требует 200 мм по бокам, 300 мм сверху, 150 мм сзади, 50 мм спереди.',
  'R6: по бокам 42 мм; над верхним габаритом Katana 124 мм. Доступ к ручкам требует примерки.',
  'Эти зазоры меньше инструкции. Нельзя считать проект согласованным для эксплуатации усилителя.',
  'AIRSTEP сдвинут вперёд: до продолжения низа K около 123 мм. Удобство ноги требует примерки.'
 ]
 for j,line in enumerate(notes): text(c,40,345-j*27,line,10,j in [5,7])
 text(c,40,75,'Источник: BOSS KATANA MkII Owner’s Manual, разделы размещения и задней панели.',9)
 c.linkURL(D['sources']['boss'],(40,68,1000,88)); text(c,40,52,'XSONIC: xsonicaudio.com/pages/airstepkatedition. Портовая схема не является сверловочным шаблоном.',9)
 c.save()

models={}; reports={}
for key,profile in D['profiles'].items():
 polys={'B':profiles(profile['formula'])}
 for part in D['parts'][2:]:
  w,h=part['size']; polys[part['code']]=tabletop(w,h,part['cornerRadius']) if part.get('cornerRadius') else rect(w,h)
 layout=[{'id':i,'code':code,'rotation':r,'poly':placed(polys[code],x,y,r)} for i,code,x,y,r in PACK]
 boxes=[bbox(i['poly']) for i in layout]; gaps=[]
 for i,a in enumerate(boxes):
  assert a[0]>=6 and a[1]>=6 and a[2]<=W-6 and a[3]<=H-6
  for b in boxes[i+1:]:
   dx=max(0,a[0]-b[2],b[0]-a[2]); dy=max(0,a[1]-b[3],b[1]-a[3]); gaps.append(math.hypot(dx,dy))
 assert min(gaps)>=6-1e-6
 report={'layoutStatus':'PASS','partsCount':len(layout),'minimumBoundingBoxGapMM':round(min(gaps),6),'marginMM':6,'utilizationPercent':round(sum(area(i['poly']) for i in layout)/(W*H)*100,2),'manufacturingRelease':False}
 report['geometrySHA256']=hashlib.sha256(json.dumps(polys,sort_keys=True).encode()).hexdigest()
 m={'polygons':polys,'layout':layout,'verification':report}; models[key]=m; reports[key]=report
 suffix='' if key=='flow' else '_'+key
 (OUT/f'guitar_stand_layout_2440x1220{suffix}.svg').write_text(svg(layout))
 (OUT/f'guitar_stand_layout_2440x1220{suffix}.dxf').write_text(dxf([('SHEET',rect(W,H))]+[(f'CUT_{i["id"]}',i['poly']) for i in layout]))
 (OUT/f'guitar_stand_parts{suffix}.dxf').write_text(dxf([(f'MASTER_{code}',placed(p,j*700,0,0)) for j,(code,p) in enumerate(polys.items())]))
 pdf(OUT/f'guitar_stand_drawings{suffix}.pdf',key,m)
 # OpenSCAD uses exactly the same sampled outlines and transforms as the browser.
 lines=['// R5. Millimetres. Nominal assembly; dado machining not modelled.']
 for part in D['parts']:
  p=polys[part['code']]; x,y,z=part['pos']; w,h=part.get('size',[420,D['sideHeight']])
  if part['plane']=='side': matrix=[[0,0,1,x],[0,1,0,y],[1,0,0,z],[0,0,0,1]]
  elif part['plane']=='vertical':
   a=math.radians(part['rotation'][0]);co,si=math.cos(a),math.sin(a)
   matrix=[[1,0,0,x-w/2],[0,co,-si,y-co*h/2+si*T/2],[0,si,co,z-si*h/2-co*T/2],[0,0,0,1]]
  else:
   a=math.radians(part['rotation'][0]); co,si=math.cos(a),math.sin(a)
   matrix=[[1,0,0,x-w/2],[0,-si,co,y+si*h/2-co*T/2],[0,co,si,z-co*h/2-si*T/2],[0,0,0,1]]
  lines.append(f'multmatrix({json.dumps(matrix)}) linear_extrude(height={T}) polygon({json.dumps(p)});')
 (ROOT/'cad'/f'guitar_stand{suffix}.scad').write_text('\n'.join(lines))
(OUT/'model.json').write_text(json.dumps({**D,'variants':models},ensure_ascii=False,indent=2))
(OUT/'verification.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
print(json.dumps(reports,ensure_ascii=False,indent=2))
