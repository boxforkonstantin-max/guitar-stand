#!/usr/bin/env python3
"""Export D2, including screening calculations and release hold points."""
from pathlib import Path
import json, math, html, csv
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from d2_geometry import P,J,model,calc,add,mul
from d2_procurement import estimate,rows,hardware,services,materials,retail_total,workshop_total
R=Path(__file__).resolve().parent; O=R/'output-d2'; O.mkdir(exist_ok=True); (O/'pdf').mkdir(exist_ok=True)
def dump(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
def outline(p):
 if 'notch' not in p:return [[0,0],[p['w'],0],[p['w'],p['h']],[0,p['h']]]
 s=p['notch'];a=s['start'];cy=s['center'];r=s['radius']
 return [[0,0],[p['w'],0],[p['w'],cy-r],[a,cy-r]]+[[a+r*math.cos(-math.pi/2-i*math.pi/40),cy+r*math.sin(-math.pi/2-i*math.pi/40)] for i in range(41)]+[[p['w'],cy+r],[p['w'],p['h']],[0,p['h']]]
for p in P:p['outline']=outline(p)
# Mechanical screening independent of paired-hole generation.
errors=[]
for j in J:
 hs=[h for pid in [j['head'],j['mate']] for p in P if p['id']==pid for h in p['holes'] if h['joint']==j['id']]
 if len(hs)!=2:errors.append(j['id']+' hole pair count')
 elif any(abs(hs[0]['world'][i]+16*j['dir'][i]-hs[1]['world'][i])>1e-6 for i in range(3)):errors.append(j['id']+' alignment')
for p in P:
 for i,a in enumerate(p['holes']):
  for b in p['holes'][i+1:]:
   # Coaxial overlap and duplicate entries (perpendicular intersections checked separately).
   if a['dir']==b['dir'] and sum((a['local'][k]-b['local'][k])**2 for k in range(3))<1e-8:errors.append('duplicate '+a['id']+' '+b['id'])
assert not errors,errors
# Shelf packing: 4 mm saw kerf, 10 mm sheet trim, white decor (rotation allowed).
nest=[];shelves=[]
for p in sorted([p for p in P if p['t']==16],key=lambda p:-min(p['w'],p['h'])):
 w,h=max(p['w'],p['h'])-.8,min(p['w'],p['h'])-.8
 row=next((s for s in shelves if s['height']>=h and s['x']+w<=2490),None)
 if row is None:
  yy=10+sum(s['height']+4 for s in shelves);row=dict(x=10,y=yy,height=h);shelves.append(row)
 nest.append(dict(id=p['id'],x=round(row['x'],2),y=round(row['y'],2),w=w,h=h,rotated=p['w']<p['h']));row['x']+=w+4
assert all(n['x']+n['w']<=2490 and n['y']+n['h']<=1820 for n in nest)
for i,a in enumerate(nest):
 for b in nest[i+1:]:
  assert a['x']+a['w']+3.99<=b['x'] or b['x']+b['w']+3.99<=a['x'] or a['y']+a['h']+3.99<=b['y'] or b['y']+b['h']+3.99<=a['y']
dump('nesting.json',dict(sheet=[2500,1830,16],kerf=4,trim=10,parts=nest));dump('estimate.json',estimate)
style='<style>body{font:16px system-ui;color:#172f34;max-width:1100px;margin:32px auto;padding:0 20px;line-height:1.5}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #ccd5d4;text-align:left;vertical-align:top}small{display:block;color:#536569}a{color:#075975}.scroll{overflow:auto}@media print{body{font-size:10px}}</style>'
ht='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>D2 — фурнитура и смета</title>'+style+'<a href="../d2.html">← Модель D2</a><h1>Фурнитура и стоимость D2</h1><p>Проверка каталогов: 12 октября 2026. Цены без доставки. Это расчёт бюджета, не счёт поставщика.</p>'
ht+=f'<p>Фурнитура: <b>{hardware:,.2f} ₽</b>. С изготовлением и целыми розничными упаковками: <b>{retail_total:,.2f} ₽</b>. Сценарий цеха с метизами поштучно: <b>{workshop_total:,.2f} ₽</b> — предварительно.</p><p>{html.escape(estimate["caveat"])}</p><div class="scroll"><table><tr><th>Позиция / ссылка на товар</th><th>Нужно</th><th>Покупка</th><th>Сумма, ₽</th></tr>'
for r in rows:ht+=f'<tr><td>{r["id"]} · <a href="{html.escape(r["url"],quote=True)}">{html.escape(r["name"])}</a><small>{html.escape(r["note"])}</small></td><td>{r["required"]}</td><td>{r["purchase"]}</td><td>{r["price_rub"]:.2f}</td></tr>'
ht+='</table></div><h2>Материалы и работы</h2><table>'
for r in materials+services:
 title=f'<a href="{r[2]}">{html.escape(r[0])}</a>' if r[2] else html.escape(r[0])
 ht+=f'<tr><td>{title}<small>{html.escape(r[3]) if len(r)>3 else ""}</small></td><td>{r[1]:.2f} ₽</td></tr>'
ht+='</table><h2>Сборка без лишних покупок</h2><p>Отдельные ручка, петли, газлифт и доводчик не нужны. Ручка фрезерована в фасаде. Направляющие имеют полный ход и рычаги снятия. Площадка AIRSTEP снимается руками и работает на полу.</p><p>Сменная плашка прежней версии удалена: теперь есть нижние опоры гитары, вилка и ремешок. Подвешивать вес гитары к вилке нельзя.</p><p>Обязательная страховка от опрокидывания: два анкера через верхнюю заднюю связь и прокладки. Чертёж подходит только для здорового бетона C20/25; для другой стены требуется другой монтажный узел.</p><p>Не включены: '+', '.join(estimate['excluded'])+'.</p><p><a href="pdf/workstation_D2.pdf">Чертежи и контрольная сборка</a> · <a href="estimate.json">Исходные суммы</a></p></html>'
(O/'hardware.html').write_text(ht)
dump('model.json',model);dump('calculations.json',calc)
with (O/'drilling.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['part','hole','u_mm','v_mm','n_mm','dir_u','dir_v','dir_n','diam_mm','depth_mm','countersink_diam_mm','joint','operation'])
 for p in P:
  for h in p['holes']:w.writerow([p['id'],h['id'],*h['local'],*h['dir'],h['diam'],h['depth'],h['cs'],h['joint'],h['job']])
sc=['// D2 mm. Screening only; see release holds in PDF.','$fn=64;']
for p in P:
 mat=[[p[k][i] for k in ['u','v','n']]+[p['origin'][i]] for i in range(3)]+[[0,0,0,1]]
 sc.append(f"// {p['id']}\nmultmatrix({mat}) difference() {{ linear_extrude({p['t']}) polygon({p['outline']});")
 for h in p['holes']:
  d=h['dir'];rot=[0,90,0] if d[0]==1 else [0,-90,0] if d[0]==-1 else [-90,0,0] if d[1]==1 else [90,0,0] if d[1]==-1 else [0,0,0] if d[2]==1 else [180,0,0]
  start=[h['local'][i]-d[i]*.01 for i in range(3)]
  sc.append(f"translate({start}) rotate({rot}) cylinder(d={h['diam']},h={h['depth']+.02});")
  if h['cs']:sc.append(f"translate({start}) rotate({rot}) cylinder(d1=10,d2=7,h=1.5);")
 for s in p['slots']:
  off=[(s['length']-s['width'])/2,0] if s['axis']=='u' else [0,(s['length']-s['width'])/2]
  sc.append('hull(){')
  for sign in [-1,1]:sc.append(f"translate([{s['x']+sign*off[0]},{s['y']+sign*off[1]},-.01]) cylinder(d={s['width']},h={p['t']+.02});")
  sc.append('}')
 sc.append('}')
(O/'assembly.scad').write_text('\n'.join(sc))
def pair(c,v):return f'{c}\n{v}\n'
dx=pair(0,'SECTION')+pair(2,'HEADER')+pair(9,'$INSUNITS')+pair(70,4)+pair(0,'ENDSEC')+pair(0,'SECTION')+pair(2,'ENTITIES')
def line(lay,x,y,xx,yy):return pair(0,'LINE')+pair(8,lay)+pair(10,x)+pair(20,y)+pair(11,xx)+pair(21,yy)
for i,p in enumerate(P):
 ox=i%4*1000;oy=i//4*950;pts=p['outline']
 for a,b in zip(pts,pts[1:]+pts[:1]):dx+=line(p['id']+'_FINISHED',ox+a[0],oy+a[1],ox+b[0],oy+b[1])
 for h in p['holes']:
  lay=p['id']+('_FACE' if h['dir'][2] else '_EDGE_REF')+f"_D{h['diam']}_DEPTH{h['depth']}"
  dx+=pair(0,'CIRCLE' if h['dir'][2] else 'POINT')+pair(8,lay)+pair(10,ox+h['local'][0])+pair(20,oy+h['local'][1])
  if h['dir'][2]:dx+=pair(40,h['diam']/2)
 for s in p['slots']:
  r=s['width']/2;d=(s['length']-s['width'])/2;pts=[]
  for n in range(129):
   a=2*math.pi*n/128;x=r*math.cos(a);y=r*math.sin(a)
   if s['axis']=='u':x+=d if x>=0 else -d
   else:y+=d if y>=0 else -d
   pts.append([ox+s['x']+x,oy+s['y']+y])
  for a,b in zip(pts,pts[1:]):dx+=line(p['id']+'_SLOT',*a,*b)
dx+=pair(0,'ENDSEC')+pair(0,'EOF');(O/'details.dxf').write_text(dx)

pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
c=canvas.Canvas(str(O/'pdf/workstation_D2.pdf'),pagesize=(1190.55,841.89));page=0
def text(x,y,s,size=12):
 c.setFillColorRGB(.07,.12,.14);c.setFont('Arial',size);c.drawString(x,y,str(s))
def new(title):
 global page
 if page:c.showPage()
 page+=1;text(35,805,'WORKSTATION / D2 / 12.10.2026',12);text(35,768,title,22)
 c.setStrokeColorRGB(.6,.65,.65);c.line(35,748,1150,748)
 text(35,25,'D2 - проект для контрольного образца. Не серийный допуск. Размеры мм; сверить контрольные условия.',10);text(1100,25,page,10)
def lines(rows,y=715):
 for s in rows:text(35,y,s,12);y-=27
new('Что изменилось и условия выпуска')
lines(['Корпус 654 x 360 x 800; с боковой опорой гитары общая ширина 834. Высота без мягких подпятников.',
 'Плашки A больше нет. Гитара стоит на нижних мягких опорах, гриф удерживают вилка GN и ремешок.',
 'Ящик на BOYARD DB4501Zn/300: боковой зазор 12,7 мм, полный ход 300 мм, съёмный педалборд внутри.',
 'Нажатие ногой допускается только на вынутой площадке, стоящей на полу. На выдвинутый ящик не наступать.',
 'Полка K опирается на два ребра KF/KR высотой 80 мм. ВСЕ детали - ЛДСП 16 мм, один лист.',
 'K: верх 236; верх Katana 634; до столешницы 150. AIRSTEP хранится на высоте 90.',
 'Чистовые размеры после кромки 0,4 мм. Распил прямоугольников: обе оси минус 0,8 мм.',
 'GN: паз открыт наружу, R33, центр дуги (85;80); оклеить/закрыть торец, мягкая накладка 3 мм.',
 'Все материалы должны отвечать принятым минимальным E/прочности; это проверяет паспорт выбранной плиты.',
 'КОНТРОЛЬНЫЕ УСЛОВИЯ: актуальная присадка направляющих, крепление к стене, образец гитары, нагрузочная проба.',
 'Устойчивость при толчке 50 Н не обеспечена во всех состояниях: требуется противоопрокидывающая связь.',
 'Вентиляция по поручению владельца отложена. Этот выпуск не разрешает эксплуатацию усилителя в нише.',
 'Чертежи и 3D получены из d2_geometry.py; R6 не изменён. Конструкция не является точной копией On-Stage.'])
new('Ящик: монтаж и последовательность открывания')
lines(['1. Направляющие установить вертикально на боковины; не класть плашмя под дно.',
 '2. Проём корпуса 622. Наружная ширина ящика 596,6 = 622 - 2 x 12,7; контролировать после кромления.',
 '3. Перед направляющей Z32, линия крепежа Y92. Боковины ящика 300 x 90 x 16.',
 '4. Корпусные пилоты: Z64 и 203,5. На ящике: Z104, 232, 296. Ø2,5 глубина 12 с пласти.',
 '5. Координаты по копии схемы DB4501 редакции 2014. Другие каталоги имеют отличия до 1 мм.',
 '   До серийного сверления наложить купленную направляющую на шаблон 1:1; не сверлить по названию товара.',
 '6. Крепёж: шуруп с полукруглой головкой 3,5x16; головка не должна задевать подвижный профиль.',
 '7. Потянуть за прорезь фасада: весь ящик перемещается на 300 мм. Направляющие имеют штатный упор.',
 '8. Взять педалборд PB за боковые края, приподнять выше бортов ящика и поставить на пол.',
 '9. Кабель USB: свободная петля не менее 700 мм, не попадает в шарики и под ножки.',
 '10. Для снятия самого ящика использовать рычаги расцепления направляющих; петли и доводчик не нужны.',
 '11. Обратный порядок: поставить педалборд на дно QB, уложить кабель, задвинуть ящик без усилия.',
 'Не считать паспортные 15 кг направляющих разрешением нажимать на них ногой.'])
new('Гитара: опоры и удержание грифа')
lines(['GB опирается на общие планки E1/E2. Вес гитары передаётся на пол, а не на верхнюю вилку.',
 'G1/G2 поддерживают низ корпуса; между ними 50 мм для нижнего ременного пина.',
 'Предельная расчётная масса гитары 5 кг. Предварительный габарит корпуса: до 340 по Z, 60 по X.',
 'Гриф в зоне GN должен проходить в 60-мм мягкий проём без давления на струны и лады.',
 'GN поддерживают два ребра GC1/GC2. Каждое прикреплено двумя конфирматами к боковине R.',
 'Вилка крепится к рёбрам четырьмя конфирматами. Пазы 22x5 служат для ремешка шириной 16 мм.',
 'Ремешок пропустить через пазы, замкнуть перед грифом; он препятствует выпадению, а не держит вес.',
 'Мягкие накладки 3 мм закрывают опоры и кромки вилки. Клей и грубая сторона липучки не касаются гитары.',
 'Декоративная модель Ibanez условная: общая форма/геометрия конкретного инструмента не измерена.',
 'Контрольная примерка обязательна: пин не нагружен, корпус стоит устойчиво, покрытие совместимо с накладкой.',
 'Расчёт вилки: 30 Н на плече 160 = 4800 Н·мм; при базе крепежа 44 мм верхний винт воспринимает около 55 Н.',
 'Прочность вырыва конфирматов из фактической ЛДСП не известна: выполнить пробу вилки 60 Н без инструмента.',
 'Сначала испытывать эквивалентом груза, не инструментом. Не подвешивать инструмент за GN.'])
new('Расчёт: полка и педалборд')
s=calc['shelf'];b=calc['pedalboard'];q=calc['drawer']
lines(['Модель усиления: ОДНО ребро L622, b16, h80 несёт все 20 кг в центре; второе не учитываем.',
 'E = 1600 Н/мм², предел изгиба 11 МПа, коэффициент 3. Требовать паспорт фактической плиты.',
 'I = b h³ / 12; M = P L / 4; sigma = M / (b h² / 6); f = P L³ / (48 E I).',
 f"Напряжение {s['stress_MPa']} МПа < {s['allowable_MPa']} МПа; мгновенный прогиб {s['short_deflection_mm']} мм.",
 f"Условный множитель ползучести 3: {s['long_deflection_mm']} мм < L/200 = {s['deflection_limit_mm']} мм.",
 'Плита K между рёбрами: пролёт 328, ширина распределения 470; 20 кг. Составная работа не учитывается.',
 'Для локальных точечных нагрузок на плиту нужен отдельный расчёт; здесь принят габарит Katana.',
 f"Педалборд на полу: нагрузка 300 Н по полосе 70 мм, пролёт 140 мм: sigma {b['stress_MPa']} МПа, f {b['deflection_mm']} мм.",
 '300 Н - выбранное проектное усилие нажатия; это не разрешение вставать всем весом.',
 f"Ящик с площадкой и AIRSTEP: древесина + педаль {q['estimated_wood_and_pedal_kg']} кг, паспорт пары 15 кг.",
 'Фурнитура и дополнительное содержимое: суммарная масса подвижного узла не более 10 кг.',
 'Соединения ЛДСП и накладки требуют контрольной сборки: расчёт балки не проверяет вырыв/смятие/расшатывание.'])
new('Устойчивость: десять состояний')
text(35,715,'Katana / ящик открыт / гитара     Масса    Xcg / Zcg      Mвперёд    Fкр на высоте 800',12)
for i,(key,v) in enumerate(calc['cases'].items()):
 flags=key.split('_');name=('Пустой / '+('открыт' if key=='empty_open' else 'закрыт')) if key.startswith('empty') else ' / '.join('да' if flags[j]=='True' else 'нет' for j in [1,3,5])
 text(35,676-i*30,f"{name:24}   {v['mass_kg']:5.2f} кг     {v['cg_mm'][0]:5.1f} / {v['cg_mm'][2]:5.1f}     {v['restoring_Nm']['front']:5.2f} Нм     {v['critical_horizontal_force_at_800_N']['front']:5.1f} Н",12)
lines(['Опорный прямоугольник: X0..834, Z20..340. Плотность 600 кг/м³; масса фурнитуры не учтена.',
 'М = Σ m g (Zcg - 20) / 1000; Fкр = М / 0,8. Скольжение и динамика не включены.',
 'Открывание за низкую ручку безопаснее толчка столешницы: сравнить момент 30 Н x 0,092 м.',
 'Случай без Katana не проходит 50 Н сверху. Без крепления к стене производственный допуск НЕ выдаётся.',
 'Первые 8 случаев включают ноутбук и AIRSTEP; последние 2 - полностью без техники.',
 'Сверления не вычтены из массы; центры фигур приближены. Для допуска нужна контрольная проба.'],y=335)
new('Стеновое крепление / только бетон C20/25')
lines(['Два fischer SXRL 10x160 FUS (522724), две шайбы DIN9021 M10, шесть прокладок W 50x50x16.',
 'Координаты отверстий в U: мировой X100 и X554, Y720, вход Z344; Ø11 сквозное.',
 'За каждым отверстием собрать три прокладки: 48 мм между задней гранью корпуса Z360 и стеной Z408.',
 'Древесина 16+48=64; шайба 2,5; фактическое заглубление дюбеля около 93,5 мм.',
 'Бур Ø10. Минимум 170 мм от плоскости опоры головки (около 104 мм в бетоне). Удалить пыль.',
 'Перед сверлением проверить отсутствие проводки/труб. Не считать штукатурку несущим бетоном.',
 'Если слой штукатурки уменьшает заделку ниже 90 мм, этот узел неприменим без пересчёта.',
 'Принять стену толщиной не менее 150 мм, до края бетона не менее 140 мм; межосевое расстояние 454 мм.',
 'Расчётное требование: 200 Н на высоте 800 дают 160 Нм; связь на Y720 воспринимает 222,2 Н суммарно.',
 'Учитывать неравномерность: каждый анкер и его соединение с U должны переносить не менее 223 Н.',
 'Это требование к соединению, а не подтверждённая несущая способность неизвестной стены.',
 'Приёмка: безопасная проба 300 Н на связь, без деформации/вырыва. Стойку не использовать без крепления.',
 'Гипсокартон, газоблок, пустотелый кирпич: монтаж по этому листу запрещён; нужен иной анкерный узел.'])
text(35,330,'Источники: fischer SXRL, ETA-07/0121, таблица допускаемых нагрузок; EGGER P2, паспорт 08.04.2026.',11)
text(35,306,'Каталог SXRL: 2,58 кН растяжения в бетоне при h70 для групповых креплений; не допуск всей стойки.',11)
c.linkURL('https://www.fischerfixing.ru/wp-content/uploads/2026/02/buklet-sxrl.pdf',(35,325,1100,345),relative=0)
c.linkURL('https://www.egger.com/get_download/6603a8d4-4c68-446d-b77a-193672c87f5a/Technical_Datasheet_Eurospan_E1_P2.pdf',(35,300,1100,320),relative=0)
new('Габариты сборки / проекции (справочные, размеры по деталям)')
for title,axes,ox in [('Спереди',(0,1),45),('Справа',(2,1),600)]:
 text(ox,715,title,14);scale=.64;oy=150
 for p in P:
  vs=[add(p['origin'],add(mul(p['u'],u),add(mul(p['v'],v),mul(p['n'],n)))) for u in [0,p['w']] for v in [0,p['h']] for n in [0,p['t']]]
  a,b=axes;x0=min(v[a] for v in vs);x1=max(v[a] for v in vs);y0=min(v[b] for v in vs);y1=max(v[b] for v in vs)
  c.setStrokeColorRGB(.25,.3,.3);c.rect(ox+x0*scale,oy+y0*scale,max(.4,(x1-x0)*scale),max(.4,(y1-y0)*scale))
 text(ox,100,'Корпус H800; полка Katana Y236; столешница Y800.',11)
text(45,70,'Ширина корпуса 654; основание с гитарой 834; глубина 360; стена Z408; ручка на фасаде.',11)
new('Раскрой ЛДСП 16 мм / 1 лист 2500 x 1830')
scale=.32;ox=40;oy=90;c.rect(ox,oy,2500*scale,1830*scale)
for n in nest:
 c.setFillColorRGB(.9,.9,.85);c.rect(ox+n['x']*scale,oy+n['y']*scale,n['w']*scale,n['h']*scale,fill=1)
 text(ox+(n['x']+3)*scale,oy+(n['y']+n['h']/2)*scale,n['id'],8)
text(860,680,'Пропил 4 мм; обрезка 10 мм.',11);text(860,650,'Белый декор без направления.',11);text(860,620,'Координаты: nesting.json.',11)
text(860,580,'Все 30 деталей - 16 мм.',11);text(860,550,'Рёбра KF/KR входят в лист.',11)
text(35,65,'Малые детали W вырезать из укрупнённой заготовки с безопасной фиксацией; не держать руками у пилы.',10)
for start in range(0,len(P),21):
 new('Деталировка и кромка')
 text(35,717,'ID       Деталь                                      Чистовой размер        Распил             Толщина',12)
 for i,p in enumerate(P[start:start+21]):
  y=685-i*26;text(35,y,p['id']);text(115,y,p['name'],11);text(485,y,f"{p['w']} x {p['h']}");text(710,y,f"{p['w']-.8:.1f} x {p['h']-.8:.1f}");text(960,y,p['t'])
for p in P:
 for chunk in range(max(1,math.ceil(len(p['holes'])/18))):
  new(f"{p['id']} / {p['name']} / {p['w']} x {p['h']} x {p['t']}")
  scale=min(440/p['w'],530/p['h']);ox=65;oy=130;path=c.beginPath();pts=p['outline'];path.moveTo(ox+pts[0][0]*scale,oy+pts[0][1]*scale)
  for x,y in pts[1:]:path.lineTo(ox+x*scale,oy+y*scale)
  path.close();c.setFillColorRGB(.92,.90,.85);c.setStrokeColorRGB(.1,.15,.16);c.drawPath(path,fill=1)
  text(65,100,'(0,0): чистовой угол; u вправо, v вверх',10)
  for h in p['holes']:
   x,y,n=h['local'];c.setStrokeColorRGB(.7,.12,.06);c.circle(ox+x*scale,oy+y*scale,max(2,h['diam']*scale/2));text(ox+x*scale+3,oy+y*scale+3,h['id'].split('.')[1],7)
  for s in p['slots']:
   w,h=(s['length'],s['width']) if s['axis']=='u' else (s['width'],s['length']);c.roundRect(ox+(s['x']-w/2)*scale,oy+(s['y']-h/2)*scale,w*scale,h*scale,s['width']*scale/2)
  headings=['ID','u','v','n','Вход','Ø','Глуб.','Соедин.'];xx=[535,610,685,760,825,905,975,1050]
  for x,s in zip(xx,headings):text(x,715,s,11)
  for i,h in enumerate(p['holes'][chunk*18:chunk*18+18]):
   axis=next(k for k,d in enumerate(h['dir']) if d);face=['u','v','n'][axis]+('0' if h['dir'][axis]>0 else 'MAX')
   for x,s in zip(xx,[h['id'],*h['local'],face,h['diam'],h['depth'],h['joint'] or '-']):text(x,685-i*25,s,10)
  y=190
  for s in p['slots']:text(535,y,f"Паз ({s['x']};{s['y']}), {s['length']}x{s['width']}, ось {s['axis']}, сквозной",10);y-=20
  text(535,110,'n: пласт; u/v: торец. Глубина от поверхности входа.',10)
  text(535,90,'Ø7: зенковка Ø10 90°, 1,5 мм. Торец Ø5 глубина 38.',10)
  text(535,70,'Кромка 0,4: сверлить от чистовой базы; не зеркалить без пересчёта.',10)
for start in range(0,len(J),40):
 new('Соединения / координаты начала и направления')
 for i,j in enumerate(J[start:start+40]):text(35+(i//20)*560,710-(i%20)*29,f"{j['id']} {j['head']} → {j['mate']} {j['kind']}  {j['start']}  {j['dir']}",10)
new('Контрольный образец: что должен проверить изготовитель')
lines(['1. Размеры после кромления ±0,3; разность диагоналей корпуса не более 1 мм; перпендикулярность.',
 '2. Пилот/зенковку сверить на обрезке с фактическим конфирматом. Не допускать расщепления/срыва.',
 '3. Присадку направляющих проверить по приобретённой паре; ход не заедает, защёлки срабатывают.',
 '4. Подвижный узел взвесить: с содержимым ≤10 кг. 50 циклов хода без перекоса и ослабления крепежа.',
 '5. Полка: эквивалент груза 20 кг, распределённый как усилитель; измерить прогиб сразу и через 24 часа.',
 '6. Педалборд на полу: приложить 300 Н в зоне выключателей, без человека сверху; проверить трещины.',
 '7. Гитара: сначала эквивалент 5 кг на нижних опорах и 30 Н к вилке в разные стороны, затем примерка.',
 '8. Противоопрокидывающую связь выполнить до испытания толчком. Анкер подбирать под стену, не по фото.',
 '9. Стендовые пробы выполняет изготовитель безопасно, с ограждением/страховкой; инструментами не испытывать.',
 '10. Вентиляцию решить отдельно перед эксплуатацией. Не считать любой набор отверстий достаточным.',
 'Без этих проверок маркировка выпуска остаётся HOLD. Физические испытания в этой работе не выполнялись.'])
new('Фурнитура / стоимость покупки упаковок')
text(35,715,'Код / наименование',12);text(660,715,'Нужно / покупка',12);text(1050,715,'Сумма, руб.',12)
for i,r in enumerate(rows):
 y=679-i*51;text(35,y,r['id']+' / '+r['name'],11);text(660,y,f"{r['required']} / {r['purchase']}",10);text(1050,y,f"{r['price_rub']:.2f}",11)
 text(35,y-18,'Открыть карточку товара (ссылка)',9);c.linkURL(r['url'],(35,y-21,280,y-5),relative=0,thickness=0)
text(35,100,f'Фурнитура: {hardware:.2f} руб. W1 рассчитан по 2 шт.; поштучный отпуск надо подтвердить.',12)
text(35,75,'Ozon / Яндекс Маркет / РФ-поставщики. Развёрнутые условия и упаковки: output-d2/hardware.html.',11)
new('Общая смета / стоимость изготовления предварительная')
for i,r in enumerate(materials+services):
 y=700-i*45;text(35,y,r[0],12);text(950,y,f'{r[1]:.2f} руб.',12)
 if r[2]:c.linkURL(r[2],(35,y-3,800,y+13),relative=0,thickness=0)
lines([f'Фурнитура {hardware:.2f}; итог с целыми розничными упаковками: {retail_total:.2f} руб.',
 f'Сценарий цеха (метизы поштучно): {workshop_total:.2f} руб.',
 'Это не фиксированная цена заказа: ЧПУ, присадка, кромка и сборка должны попасть в предложение цеха.',
 'Доставка, монтаж в стену, техника и опциональные органайзеры не включены. Заказы не оформлялись.',
 'Не покупать 50 анкеров: если поставщик не отпускает 2, цех закупает поштучно или пересчитывает узел.'],y=235)
c.save()
dump('checks.json',dict(revision='D2',parts=len(P),joints=len(J),holes=sum(len(p['holes']) for p in P),paired_axes='PASS',bounds='PASS',duplicate_holes='PASS',nesting='PASS',release='FIRST_ARTICLE_ONLY',holds=['site anchor substrate/capacity validation','slide sample template','material certificate and physical proof tests','guitar fit and pad compatibility','ventilation deferred']))
print(json.dumps({'parts':len(P),'joints':len(J),'pages':page,'holes':sum(len(p['holes']) for p in P),'release':'FIRST_ARTICLE_ONLY'}))
