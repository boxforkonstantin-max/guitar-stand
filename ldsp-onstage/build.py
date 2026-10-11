#!/usr/bin/env python3
"""D1: independent LDSP design. All drawing/model coordinates derive here, mm."""
import json, math, html, hashlib
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parent
O=R/'output'; O.mkdir(exist_ok=True)
(O/'pdf').mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
P=[]; J=[]
def part(id,name,w,h,origin,u,v,n,group='frame'):
 p=dict(id=id,name=name,w=w,h=h,t=16,origin=origin,u=u,v=v,n=n,group=group,holes=[],slots=[])
 P.append(p);return p
X=[1,0,0];Y=[0,1,0];Z=[0,0,1]
L=part('L','Левая боковина',360,768,[0,16,0],Z,Y,X)
B=part('R','Правая боковина',360,768,[638,16,0],Z,Y,X)
T=part('T','Площадка ноутбука',654,360,[0,784,0],X,Z,Y)
D=part('D','Дно корпуса',622,360,[16,16,0],X,Z,Y)
K=part('K','Полка Katana',622,360,[16,176,0],X,Z,Y)
V=part('V','Задняя нижняя связь',622,80,[16,220,344],X,Y,Z)
U=part('U','Задняя верхняя связь',622,80,[16,680,344],X,Y,Z)
Q=part('Q','Дека съёмной кассеты',590,280,[32,40,32],X,Z,Y,'pedal')
F=part('F','Фасад кассеты',618,120,[18,36,16],X,Y,Z,'pedal')
# Full-width feet strips avoid end-grain attachment of small feet to side panels.
E1=part('E1','Передняя опорная планка',654,50,[0,0,20],X,Z,Y)
E2=part('E2','Задняя опорная планка',654,50,[0,0,290],X,Z,Y)
A=part('A','Сменная плашка держателя',160,200,[654,544,100],Z,Y,X,'guitar')
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(a,b):return [x+y for x,y in zip(a,b)]
def mul(a,s):return [x*s for x in a]
def local(p,g):
 d=[g[i]-p['origin'][i] for i in range(3)]
 return [dot(d,p[k]) for k in ['u','v','n']]
def hole(p,start,direction,diam,depth,job,joint='',cs=0):
 l=local(p,start); dr=[dot(direction,p[k]) for k in ['u','v','n']]
 assert sum(abs(x) for x in dr)==1
 ext=[p['w'],p['h'],16]
 assert all(-.001<=l[i]<=ext[i]+.001 for i in range(3)),(p['id'],l)
 axis=next(i for i,x in enumerate(dr) if x)
 assert abs(l[axis]-(0 if dr[axis]>0 else ext[axis]))<.001,(p['id'],l,dr)
 assert depth<=ext[axis]+.001
 for i in range(3):
  if i!=axis:assert diam/2<=l[i]<=ext[i]-diam/2,(p['id'],l)
 rec=dict(id=f"{p['id']}.{len(p['holes'])+1:02}",local=l,dir=dr,world=start,worldDir=direction,diam=diam,depth=depth,job=job,joint=joint,cs=cs)
 p['holes'].append(rec);return rec
def joint(head,mate,start,direction,kind='C7'):
 # head always 16 mm; receiver pilot 38 mm gives 4 mm drill clearance for 7x50.
 id=f'J{len(J)+1:02}'; end=add(start,mul(direction,16))
 dia,dep=(7,38) if kind=='C7' else (4.5,12)
 a=hole(head,start,direction,dia,16,'сквозное',id,10 if kind=='C7' else 0)
 b=hole(mate,end,direction,5 if kind=='C7' else 2.5,dep,'глухое',id)
 assert all(abs(a['world'][i]+direction[i]*16-b['world'][i])<1e-8 for i in range(3))
 J.append(dict(id=id,head=head['id'],mate=mate['id'],start=start,dir=direction,kind=kind))
for side,x,dx in [(L,0,1),(B,654,-1)]:
 for shelf,cy in [(D,24),(K,184)]:
  for z in [50,180,310]:joint(side,shelf,[x,cy,z],[dx,0,0])
 for rear in [V,U]:
  for yy in [20,60]:joint(side,rear,[x,rear['origin'][1]+yy,352],[dx,0,0])
for side,x in [(L,8),(B,646)]:
 for z in [50,180,310]:joint(T,side,[x,800,z],[0,-1,0])
for x in [82,222,432,572]:joint(F,Q,[x,48,16],[0,0,1])
# Feet strips screwed down through floor, not through a 16 mm edge.
for rail,z in [(E1,45),(E2,315)]:
 for x in [70,327,584]:joint(D,rail,[x,32,z],[0,-1,0],'S4')
for z in [120,240]:
 for y in [584,704]:
  for p,xx in [(B,638),(A,654)]:hole(p,[xx,y,z],X,6.5,16,'сквозное M6')
# Adapter universal slots are optional; no claim of fit to any marketplace hanger.
A['slots']=[dict(x=50,y=100,length=60,width=5.5,axis='v'),dict(x=110,y=100,length=60,width=5.5,axis='v')]
F['slots']=[dict(x=309,y=85,length=110,width=24,axis='u')]
Q['slots']=[dict(x=295,y=220,length=160,width=20,axis='u')]
for x in [62,592]:
 for z in [62,282]:hole(Q,[x,40,z],Y,2.5,10,'пилот ножки; сверить шуруп')

warnings=[
 'D1 - инженерный прототип. НЕ ВЫПУСК В ПРОИЗВОДСТВО: вентиляция отложена, нагрузки/устойчивость не испытаны.',
 'Компактность согласована; зазоры руководства BOSS не соблюдены. Отверстия вентиляции не добавлены.',
 'Все размеры деталей - после кромления. ПВХ 0,4 мм по 4 сторонам; заготовка на 0,8 мм меньше по каждой оси.',
 'Координаты присадки от чистового угла. Выполнять после кромления либо пересчитать базу на 0,4 мм.',
 'Конфирмат 7x50: пласт Ø7 сквозное + зенковка Ø10 90° до заподлицо; торец Ø5 глубина 38.',
 'Сначала пробное соединение на обрезке выбранной ЛДСП/винта. Фактическая толщина плиты должна быть 16 мм.',
 'Кассета извлекается целиком: ножки приподнять над дном, поставить на пол. Не нажимать ногой внутри корпуса.',
 'Плашка A - интерфейс держателя, не готовый держатель гитары. Его посадку/высоту проверить по образцу.',
 'Гитару не подвешивать до проверки держателя и устойчивости, в том числе при снятой Katana.',
 'Прямые углы ЛДСП: снять остроту кромки. Все открытые торцы прорезей герметизировать/облицевать.'
]
links=[
 ['C7','Конфирмат 7x50',30,'шт','https://www.ozon.ru/product/konfirmat-7h50-mm-10sht-mebelnyy-vint-styazhka-golovka-potaynaya-pod-shestigrannik-evrovint-1317687131/','3 упаковки по 10; проверить геометрию головки; ориентир 249–279 руб из индекса'],
 ['C0','Заглушка под конфирмат',30,'шт','https://www.ozon.ru/search/?text=заглушка+конфирмат+7x50+черная','Поисковая ссылка; цвет по ЛДСП'],
 ['S4','Шуруп 4x30, полукруглая головка',6,'шт','https://market.yandex.ru/search?text=шуруп+4х30+полукруглая+головка','Поиск; крепление опорных планок; пилот Ø2,5x12'],
 ['M6','Болт M6x45 DIN 912',4,'шт','https://market.yandex.ru/search?text=болт+М6х45+DIN+912','Поиск; плашка A; шайбы с двух сторон, гайка с нейлоном'],
 ['W6','Шайба увеличенная M6 DIN 9021',8,'шт','https://www.ozon.ru/search/?text=шайба+М6+DIN+9021','Поиск; наружный диаметр 18 мм'],
 ['N6','Гайка M6 DIN 985',4,'шт','https://market.yandex.ru/search?text=гайка+М6+DIN+985','Поиск; самоконтрящаяся'],
 ['P8','Резиновая ножка высота 8 мм',4,'шт','https://www.ozon.ru/search/?text=ножка+резиновая+8+мм+под+шуруп','Поиск; дека кассеты; Ø20–25; шуруп с заходом в плиту 10–12 мм, подобрать к ножке'],
 ['S3','Шуруп ножки Ø3–3,5',4,'шт','https://market.yandex.ru/search?text=шуруп+3.5х16+полукруглая','Поиск; длина = толщина ножки под головкой + 10–12 мм; НЕ назначать 16 мм вслепую'],
 ['EP','Нескользящая прокладка EPDM 1 мм',0.066,'м²','https://www.ozon.ru/search/?text=резина+EPDM+лист+1+мм','Поиск; под планки E1/E2, 2 полосы 654x50; увеличит высоту корпуса примерно на 1 мм'],
 ['VC','Липучка 25 мм крючок + петля',1,'м комплекта','https://www.ozon.ru/category/lenta-lipuchka-samokleyuschayasya/','Категория, не выбранный SKU; на AIRSTEP 2 полосы 250 мм; не закрыть винты/ножки'],
 ['VT','Стяжка-липучка 150x12',8,'шт','https://m.integration.vs.market.yandex.net/card/mnogorazovaya-styazhka-lipuchka-dlya-provodov-i-kabeley-150kh12-mm-tsvet-chernyy-20-sht/102473445874','Карточка: упаковка 20, ориентир 129 руб с Пэй из индекса'],
 ['GH','Мягкий держатель гитары (кандидат)',1,'шт','https://www.ozon.ru/product/gitarnyy-kryuchok-veshalka-nastennyy-neskolzyashchiy-derzhatel-podstavka-dlya-gitary-ukulele-2675654515/','335–353 руб из индекса; НЕ проверена посадка на A и совместимость с покрытием гитары'],
 ['M5','Болт M5, шайбы, гайки держателя',2,'компл','https://market.yandex.ru/search?text=болт+М5+гайка+шайба','Длину выбрать по толщине основания держателя + 16 мм плашки + шайбы/гайка; не выпускать до выбора GH'],
 ['HK','Крючок для наушников на струбцине',1,'шт','https://www.ozon.ru/search/?text=держатель+наушников+струбцина+16+мм','Поиск; зажим должен принимать столешницу 16 мм, мягкие накладки; без сверления корпуса'],
 ['ED','ПВХ кромка 0,4 мм',round(sum(2*(p['w']+p['h']) for p in P)/1000*1.1,1),'м с 10% запасом','https://market.yandex.ru/search?text=кромка+ПВХ+0.4+22+мм','Декор в цвет; обработка на производстве'],
 ['SE','Герметизация торцов прорезей',1,'операция','https://market.yandex.ru/search?text=кромка+для+ЛДСП','Производственный расходник согласовать с технологом; открытый торец не оставлять']
]
assert sum(j['kind']=='C7' for j in J)==30
model=dict(revision='D1',units='mm',envelope=[654,800,360],parts=P,joints=J,warnings=warnings,hardware=links,equipment=[dict(id='amp',name='Katana-50 MkII',size=[470,398,238],pos=[92,192,45]),dict(id='pedal',name='AIRSTEP Kat Edition',size=[300,45,70],pos=[177,56,85]),dict(id='laptop',name='MacBook Air 15 (закрытый габарит)',size=[340.4,11.5,237.6],pos=[156.8,800,50])])
(O/'model.json').write_text(json.dumps(model,ensure_ascii=False,indent=2))
# OpenSCAD with actual subtractive face AND edge bores.
sc=['// D1, mm. Prototype: ventilation and guitar holder not released.','$fn=32;']
for p in P:
 mat=[[p[k][i] for k in ['u','v','n']]+[p['origin'][i]] for i in range(3)]+[[0,0,0,1]]
 sc.append(f"// {p['id']} {p['name']}\nmultmatrix({mat}) difference() {{ cube([{p['w']},{p['h']},16]);")
 for h in p['holes']:
  d=h['dir']; rot=[0,90,0] if d[0]==1 else [0,-90,0] if d[0]==-1 else [-90,0,0] if d[1]==1 else [90,0,0] if d[1]==-1 else [0,0,0] if d[2]==1 else [180,0,0]
  start=[h['local'][i]-d[i]*.01 for i in range(3)]
  sc.append(f"translate({start}) rotate({rot}) cylinder(d={h['diam']},h={h['depth']+.02});")
  if h['cs']:sc.append(f"translate({start}) rotate({rot}) cylinder(d1=10,d2=7,h=1.5);")
 for s in p['slots']:
  delta=(s['length']-s['width'])/2; off=[delta,0] if s['axis']=='u' else [0,delta]
  sc.append('hull(){')
  for sign in [-1,1]:sc.append(f"translate([{s['x']+sign*off[0]},{s['y']+sign*off[1]},-0.1]) cylinder(d={s['width']},h=16.2);")
  sc.append('}')
 sc.append('}')
(O/'assembly.scad').write_text('\n'.join(sc))
# DXF uses individual detail origins in mm; only face holes are circles, edge holes use POINT marks.
def pair(c,v):return f'{c}\n{v}\n'
dx=pair(0,'SECTION')+pair(2,'HEADER')+pair(9,'$INSUNITS')+pair(70,4)+pair(0,'ENDSEC')+pair(0,'SECTION')+pair(2,'ENTITIES')
for idx,p in enumerate(P):
 ox=(idx%4)*850;oy=(idx//4)*950
 points=[(0,0),(p['w'],0),(p['w'],p['h']),(0,p['h'])]
 for k,(x,y) in enumerate(points):
  x2,y2=points[(k+1)%4];dx+=pair(0,'LINE')+pair(8,p['id']+'_FINISHED_OUTLINE')+pair(10,ox+x)+pair(20,oy+y)+pair(11,ox+x2)+pair(21,oy+y2)
 for h in p['holes']:
  x,y,n=h['local'];lay=p['id']+('_FACE_' if h['dir'][2] else '_EDGE_REFERENCE_')+str(h['diam'])+'_DEPTH_'+str(h['depth'])
  dx+=pair(0,'CIRCLE' if h['dir'][2] else 'POINT')+pair(8,lay)+pair(10,ox+x)+pair(20,oy+y)
  if h['dir'][2]:dx+=pair(40,h['diam']/2)
 for s in p['slots']:
  r=s['width']/2;delta=(s['length']-s['width'])/2;pts=[]
  for i in range(66):
   theta=2*math.pi*i/65
   if s['axis']=='u': x=s['x']+r*math.cos(theta)+(delta if math.cos(theta)>=0 else -delta);y=s['y']+r*math.sin(theta)
   else:x=s['x']+r*math.cos(theta);y=s['y']+r*math.sin(theta)+(delta if math.sin(theta)>=0 else -delta)
   pts.append((x,y))
  for (x,y),(x2,y2) in zip(pts,pts[1:]):dx+=pair(0,'LINE')+pair(8,p['id']+'_SLOT_THROUGH')+pair(10,ox+x)+pair(20,oy+y)+pair(11,ox+x2)+pair(21,oy+y2)
dx+=pair(0,'ENDSEC')+pair(0,'EOF');(O/'details.dxf').write_text(dx)
# Human-readable procurement document with source types explicit.
rows=''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td><td>{c} {d}</td><td><a href="{html.escape(e)}">Открыть</a></td><td>{html.escape(f)}</td></tr>' for a,b,c,d,e,f in links)
(O/'hardware.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><title>Фурнитура D1</title><style>body{font:16px system-ui;max-width:1200px;margin:32px auto;padding:16px}td,th{padding:12px;border-bottom:1px solid #bbb;text-align:left}table{border-collapse:collapse}a{color:#064fa4}</style><h1>Фурнитура / D1</h1><p>11.10.2026. Количество на одно изделие. Поисковые ссылки не являются выбранными товарами. Цены из поискового индекса, доставка не проверена. Не полный заказ к покупке: GH, M5, ножки и их шурупы требуют сверки образцов.</p><table><tr><th>Код</th><th>Наименование</th><th>Количество</th><th>Ссылка</th><th>Примечание</th></tr>'+rows+'</table><h2>Не покупаем</h2><p>Телескопические направляющие, петли, доводчики, магнитные замки и покупную ручку: в этой конструкции их нет.</p><h2>Хранение мелочей</h2><p>1. Съёмный лоток 200×100×25 на столешнице сбоку ноутбука: самый простой. 2. Подвесной лоток под передним краем: беречь доступ к ручкам Katana. 3. Узкий лоток на верхней задней надставке: проверить экран. Это опции компоновки, не включены в деталировку D1.</p></html>')

c=canvas.Canvas(str(O/'pdf'/'workstation_D1.pdf'),pagesize=(1190.55,841.89));pw,ph=1190.55,841.89;page=0
def txt(x,y,s,size=11):
 c.setFillColorRGB(.08,.12,.14);c.setFont('Arial',size);c.drawString(x,y,str(s))
def new(title):
 global page
 if page:c.showPage()
 page+=1;c.setFillColorRGB(.08,.12,.14);txt(35,800,'WORKSTATION / ЛДСП 16 / D1',13);txt(35,766,title,23)
 c.setStrokeColorRGB(.6,.65,.66);c.line(35,745,1150,745);txt(35,25,'D1 - НЕ В ПРОИЗВОДСТВО. Вентиляция и держатель гитары не завершены. Размеры в мм.',10);txt(1090,25,f'{page}',11)
def lines(items,x=35,y=715,step=26):
 for s in items:txt(x,y,s,11);y-=step
new('Сборка и ограничения')
lines(warnings)
lines(['Габарит корпуса 654 x 360 x 800 (без мягкой прокладки под опорами).',
 'Полка Katana: верх Y192; верх усилителя Y590; до низа столешницы 194 мм.',
 'Кассета: чистый зазор до полки над AIRSTEP 75 мм; играть на полу, не внутри ниши.',
 'Модель и присадка созданы из одного build.py. Основной прототип R6 не изменён.',
 'Оси сборки: X вправо, Y вверх, Z назад. Начало: левый передний нижний угол корпуса.',
 'Элементы A/GH не определяют готовность бокового хранения: до примерки гитары НЕ использовать.'],y=430)
new('Схема компоновки / условно прозрачные виды')
def view(axes,ox,oy,s):
 for p in P:
  corners=[add(p['origin'],add(mul(p['u'],u),add(mul(p['v'],v),mul(p['n'],n)))) for u in [0,p['w']] for v in [0,p['h']] for n in [0,16]]
  a,b=axes;xs=[v[a] for v in corners];ys=[v[b] for v in corners]
  x,y=min(xs),min(ys);w,h=max(xs)-x,max(ys)-y
  c.setFillColorRGB(.91,.86,.75);c.setStrokeColorRGB(.2,.25,.27);c.rect(ox+x*s,oy+y*s,w*s,h*s,fill=1)
  txt(ox+(x+w/2)*s,oy+(y+h/2)*s,p['id'],9)
 for e in model['equipment']:
  a,b=axes;c.setFillColorRGB(.24,.27,.28);c.rect(ox+e['pos'][a]*s,oy+e['pos'][b]*s,e['size'][a]*s,e['size'][b]*s,fill=1)
view((0,1),55,155,.61);view((2,1),545,155,.61);view((0,2),795,420,.45)
txt(55,100,'Спереди: 654 x 800',14);txt(545,100,'Сбоку: глубина 360',14);txt(795,390,'Сверху',14)
new('Детали и кромление')
lines(['Кромка 0,4 мм на все 4 наружные стороны. u/v - оси чертежа детали.', 'Раскрой не оптимизирован под лист: заказать детали из остатка декора либо раскрой у исполнителя.'])
yy=640
for p in P:
 txt(40,yy,f"{p['id']:3}  {p['name']}",12);txt(390,yy,f"1 шт   {p['w']} x {p['h']} x 16",12);txt(640,yy,f"распил {p['w']-.8:.1f} x {p['h']-.8:.1f}",12);txt(925,yy,f"{len(p['holes'])} сверлений",11);yy-=35
for p in P:
 hs=p['holes']
 for chunk in range(max(1,math.ceil(len(hs)/17))):
  new(f"{p['id']} / {p['name']} / {p['w']} x {p['h']} x 16")
  scale=min(440/p['w'],540/p['h']);ox,oy=70,135
  c.setStrokeColorRGB(.15,.2,.2);c.setFillColorRGB(.97,.95,.9);c.rect(ox,oy,p['w']*scale,p['h']*scale,fill=1)
  txt(ox,oy-28,'(0,0) - чистовой угол; u вправо, v вверх',10)
  txt(ox,oy+p['h']*scale+18,f"u = {p['w']}; v = {p['h']}",12)
  for h in hs:
   x,y,n=h['local'];c.setStrokeColorRGB(.72,.18,.12);c.circle(ox+x*scale,oy+y*scale,max(2,h['diam']/2*scale));txt(ox+x*scale+4,oy+y*scale+4,h['id'].split('.')[1],8)
  for sl in p['slots']:
   w,h=(sl['length'],sl['width']) if sl['axis']=='u' else (sl['width'],sl['length'])
   c.roundRect(ox+(sl['x']-w/2)*scale,oy+(sl['y']-h/2)*scale,w*scale,h*scale,sl['width']/2*scale)
  txt(550,710,'ID       u       v       n     Вход       Ø     Глуб.     Соединение',12)
  yy=680
  for h in hs[chunk*17:(chunk+1)*17]:
   axis=next(i for i,d in enumerate(h['dir']) if d);face=['u','v','n'][axis]+('0' if h['dir'][axis]>0 else 'MAX')
   st=f"{h['id']:5}   {h['local'][0]:6g}   {h['local'][1]:6g}   {h['local'][2]:4g}   {face:5}   {h['diam']:4g}   {h['depth']:4g}      {h['joint'] or '-'}"
   txt(550,yy,st,11);yy-=25
  yy-=10
  for sl in p['slots']:
   txt(550,yy,f"Паз: центр ({sl['x']},{sl['y']}), {sl['length']} x {sl['width']}, ось {sl['axis']}, сквозной.",10);yy-=23
  lines(['n=0 / nMAX: вход с пласти; u/v: вход с соответствующего торца.', 'Ø7: зенковка Ø10 90°; Ø5 в торце: ось на половине толщины (8).', 'Глубина указана от поверхности входа, не от противоположной стороны.', 'На графике показана проекция центров. Торцевое сверление - по таблице.', 'Все отверстия на графике; эта таблица: часть '+str(chunk+1)+'.'],x=550,y=150,step=20)
new('Соединения / оси крепежа')
for i,j in enumerate(J):
 col=i//20;row=i%20;x=40+col*560;y=700-row*27
 txt(x,y,f"{j['id']}   {j['head']} → {j['mate']}   {j['kind']}   начало {j['start']}   ось {j['dir']}",11)
lines(['C7 = конфирмат 7x50; S4 = шуруп 4x30. Начало и ось в координатах сборки X/Y/Z.', 'Крепление плашки A: 4 M6x45; отверстия A.01–04 и R.14–17 соосны.', 'M6: две плиты 32 мм + шайбы с двух сторон + гайка; контролировать выход минимум двух витков.'],y=120,step=22)
new('Сборка / крепёж / контроль')
lines(['1. Закромить детали; проверить толщину и пробное соединение 7x50.',
 '2. К D снизу приложить E1/E2; 6 шурупов 4x30 через Ø4,5 в D в пилоты E1/E2.',
 '3. L/R соединить с D/K/V/U на 20 конфирматов. Пока не затягивать до конца.',
 '4. Проверить диагонали корпуса; закрепить T шестью конфирматами. Затягивать без срыва ЛДСП.',
 '5. Соединить F и Q четырьмя конфирматами. Установить четыре ножки высотой 8 мм.',
 '6. Кассету вставлять без кабелей под её ножками. При извлечении слегка приподнимать, не тянуть разъём.',
 '7. Прикрепить A четырьмя M6x45 с увеличенными шайбами с двух сторон и гайками DIN985.',
 '8. GH ставить только после проверки его основания, высоты грифа и устойчивости. Не сверлить по фото.',
 '9. Наклеить полосы липучки на деку и AIRSTEP, не перекрывая элементы обслуживания.',
 '10. Кабель USB пропустить через паз Q; оставить свободную петлю для выноса кассеты на пол.',
 '11. Провести контрольную сборку без оборудования: люфты, выход шурупов, качание, острые кромки.',
 '12. До нагрузки оборудованием проверить прочность, устойчивость и вентиляцию. Не вставать на полки.',
 'Фурнитура со ссылками: ../hardware.html. CAD с вычитанием отверстий: ../assembly.scad.',
 'DXF: контуры ЧИСТОВЫЕ; слои EDGE_REFERENCE только справочные, не траектории сверления пласти.',
 'Общая геометрия в model.json; диаметры/глубины в нём совпадают с этими таблицами.'])
c.save()
report=dict(revision='D1',parts=len(P),joints=len(J),confirmats=30,holes=sum(len(p['holes']) for p in P),checks=['local hole bounds and depth PASS','joint mating axis alignment PASS','confirmat quantity PASS'],release='NOT_FOR_MANUFACTURE',pending=['ventilation','load/stability test','guitar support fit','selected feet screw lengths','procurement availability'])
(O/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
