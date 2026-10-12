"""D3 review pack: explicit manufacturing holds, no inferred hardware drillings."""
from pathlib import Path
import json,csv,math,html
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from d3_geometry import P,J,model,calc,checks
R=Path(__file__).resolve().parent;O=R/'output-d3';O.mkdir(exist_ok=True)
def dump(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
dump('model.json',model);dump('checks.json',checks);dump('calculations.json',calc)
with (O/'drilling.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['part','hole','u','v','n','du','dv','dn','diam','depth','joint'])
 for p in P:
  for h in p['holes']:w.writerow([p['id'],h['id'],*h['local'],*h['dir'],h['diam'],h['depth'],h['joint']])
# All finished dimensions; part contours and handle openings. Hardware holes on HOLD.
def pair(c,v):return f'{c}\n{v}\n'
dx=pair(0,'SECTION')+pair(2,'HEADER')+pair(9,'$INSUNITS')+pair(70,4)+pair(0,'ENDSEC')+pair(0,'SECTION')+pair(2,'ENTITIES')
def line(layer,a,b):return pair(0,'LINE')+pair(8,layer)+pair(10,a[0])+pair(20,a[1])+pair(11,b[0])+pair(21,b[1])
for i,p in enumerate(P):
 ox=i%4*900;oy=i//4*950;pts=[[ox+x,oy+y] for x,y in p['outline']]
 for a,b in zip(pts,pts[1:]+pts[:1]):dx+=line(p['id']+'_FINISHED',a,b)
 for s in p['slots']:
  r=s['width']/2;d=(s['length']-s['width'])/2;pts=[]
  for n in range(129):
   a=2*math.pi*n/128;x=r*math.cos(a);y=r*math.sin(a)
   if s['axis']=='u':x+=d if x>=0 else -d
   else:y+=d if y>=0 else -d
   pts.append([ox+s['x']+x,oy+s['y']+y])
  for a,b in zip(pts,pts[1:]):dx+=line(p['id']+'_THROUGH_SLOT',a,b)
 for h in p['holes']:
  layer=p['id']+('_FACE' if h['dir'][2] else '_EDGE_REFERENCE')+f"_D{h['diam']}_DEPTH{h['depth']}"
  dx+=pair(0,'CIRCLE' if h['dir'][2] else 'POINT')+pair(8,layer)+pair(10,ox+h['local'][0])+pair(20,oy+h['local'][1])
  if h['dir'][2]:dx+=pair(40,h['diam']/2)
dx+=pair(0,'ENDSEC')+pair(0,'EOF');(O/'details.dxf').write_text(dx)
rows=[
 ('Конфирмат 7×50, внутренний шестигранник','34 шт.',67.32,'https://www.krepika.ru/catalog/itempage/6725/','1,98 ₽/шт. Цена в каталоге 12.10.2026.'),
 ('Саморез 4×30, головка со сферой, PZ','20 шт. ≈ 0,040 кг',50.96,'https://www.krepika.ru/catalog/itempage/7312/','1273,96 ₽/кг. Масса 0,002 кг/шт. округлена магазином; итог по весам.'),
 ('Рояльная петля 500 мм','1 шт. / резерв',150,'https://1levsha.ru/catalog/mebelnaya_furnitura/7020/','Ссылка на товар в Екатеринбурге. 150 ₽ — бюджет, не подтверждённая цена; присадка HOLD.'),
 ('Ограничители откидывания, пара','резерв',200,'','Выбрать пару под фасад ~0,6 кг; не газлифт для тяжёлой двери. Присадка HOLD.'),
 ('Магнитный фиксатор с ответной частью','1 компл. / резерв',100,'','Присадка после выбора. Не добавлять отдельную выступающую ручку.'),
 ('Мягкие привинчиваемые опоры гитары','3 шт. / резерв',1000,'https://on-stage.com/guitar-workstation-rosewood','Две нижние опоры и верхний ограничитель. Это референс, НЕ ссылка на покупку. Точный аналог ещё не выбран.'),
 ('Липучка UNIBOB 49310, 20 мм × 1 м','1 комплект',232.80,'https://lipkaya-lenta.ru/katalog/lipuchki-zastezhki/lenta-lipuchka-unibob-kruchok-petlya-samokleyashayasya.html','Ранее найденная цена, повторно не подтверждена. Для педали; к гитаре не приклеивать.'),
 ('Подпятники / мягкие накладки','резерв',104,'','Локальные подпятники, не рулон резины 6 м. На гитаре — совместимое с лаком заводское покрытие.'),
 ('Малый крепёж петли, фиксатора и держателей','резерв поштучно/весом',100,'https://www.krepika.ru/catalog/itempage/1575/','3,5×16 потай: 519 ₽/кг; количество и длины определить по фурнитуре, не покупать 250 шт.'),
 ('Страховка от опрокидывания','резерв',300,'https://www.krepika.ru/catalog/itempage/66196/','Пример местной цены: RDRp 10×160 — 49,98 ₽/шт. НЕ автоматическая замена SXRL: стена и узел не выбраны.'),
]
services=[('ЛДСП 16 мм, целый лист 2500×1830',2130),('Распил — бюджет, не заказ цеха',700),('Кромление 23,916 м × 60 ₽',1434.96),('Материал кромки — резерв',450),('108 сверлений × 25 ₽',2700),('Ручки, отверстия новой фурнитуры, доводка — резерв',1200),('Сборка и контрольные испытания — резерв',2500)]
subtotal=round(sum(r[2] for r in rows),2);total=round(subtotal+sum(r[1] for r in services),2)
dump('estimate.json',dict(date='2026-10-12',hardware=rows,services=services,hardware_budget=subtotal,total_budget=total,status='PRELIMINARY: reserves are not seller quotes; shipping and wall installation excluded'))
page='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>D3 / смета</title><style>body{font:16px system-ui;max-width:1100px;margin:30px auto;padding:0 20px;color:#172b30;background:#f7f5ef}table{border-collapse:collapse;width:100%}td,th{padding:12px;text-align:left;border-bottom:1px solid #bcc4c2}small{display:block;margin-top:6px;color:#485c60}a{color:#075b79}.scroll{overflow:auto}h1{font-size:26px}</style><a href="../d3.html">← Модель D3</a><h1>Без ящика и больших упаковок крепежа</h1><p>Цены Крепики прочитаны в каталоге 12.10.2026. Резервы подписаны отдельно. Это бюджет для согласования, не подтверждённый заказ и не окончательная спецификация.</p>'''
page+=f'<p>Фурнитура с резервами: <b>{subtotal:,.2f} ₽</b>. Вся стойка с работами: <b>{total:,.2f} ₽</b>. Без доставки и монтажа к стене.</p><div class="scroll"><table><tr><th>Позиция</th><th>Количество</th><th>Сумма, ₽</th></tr>'
for name,q,price,url,note in rows:
 title=f'<a href="{url}">{html.escape(name)}</a>' if url else html.escape(name)
 page+=f'<tr><td>{title}<small>{html.escape(note)}</small></td><td>{q}</td><td>{price:.2f}</td></tr>'
page+='</table></div><h2>Материал и работы</h2><table>'
for name,price in services:page+=f'<tr><td>{name}</td><td>{price:.2f} ₽</td></tr>'
page+='</table><h2>Что исключено</h2><p>Телескопические направляющие и короб ящика; деревянная вилка, её рёбра и боковая платформа; рулон резины; упаковки по 250 шурупов; пакет шайб на 10 штук.</p><p>Для сравнения: <a href="https://www.krepika.ru/catalog/itempage/1794/">DIN 9021 М10 — 3,74 ₽/шт.</a>; <a href="https://www.krepika.ru/catalog/itempage/48521/">SXRL T 10×160 — 267,89 ₽/шт.</a> (иная головка, чем прежний FUS). Покупать только выбранное исполнение, не смешивать дюбели и шурупы разных систем.</p><p>Ручки — сквозные пазы 110×30 мм, без покупной накладной ручки. Обработать и закрыть торец, снять острые кромки.</p><h2>Не закрыто до производства</h2><ul>'
for h in model['holds']:page+='<li>'+html.escape(h)+'</li>'
page+='</ul><p><a href="review.pdf">Размеры, механизм и контрольные условия</a></p></html>'
(O/'hardware.html').write_text(page)
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
c=canvas.Canvas(str(O/'review.pdf'),pagesize=(1190.55,841.89));number=0
def text(x,y,s,size=12):c.setFillColorRGB(.08,.16,.18);c.setFont('Arial',size);c.drawString(x,y,str(s))
def new(title):
 global number
 if number:c.showPage()
 number+=1;text(35,805,'WORKSTATION D3 / ИСПРАВЛЕННАЯ КОМПОНОВКА / 12.10.2026');text(35,766,title,22)
 c.setStrokeColorRGB(.6,.66,.66);c.line(35,749,1150,749);text(35,24,'HOLD: не передавать в производство до подбора фурнитуры и проверки её присадки. Размеры мм.',10);text(1110,24,number,10)
def lines(ss,y=715):
 for s in ss:text(35,y,s);y-=28
new('D3: дверца, съёмная площадка, мягкие держатели')
lines(['Корпус 654 x 360 x 800; закрытый фасад выступает вперёд на 18. Опоры гитары выступают вправо на 120.',
 'Старый R6 и прежние D1/D2 сохранены. D2 отклонён владельцем, его чертежи не актуальны для D3.',
 '15 деталей ЛДСП 16; 34 конфирмата 7x50 и 20 саморезов 4x30 в основных соединениях.',
 'Ручки в L/R: сквозные пазы 110x30, R15, центр u175 / v680. Чистовой верх Y711.',
 'Полка Katana горизонтальная, верх Y236; усилитель 470x398x238, масса 11,6 кг.',
 'Столешница Y800, ноутбук Air 15 помещается. До низа столешницы над Katana 150 мм.',
 'AIRSTEP Kat 300x45x70, 0,65 кг; площадка PB 500x220x16, верх в отсеке Y64.',
 'Откидная дверца F 618x100x16; ось поворота X, Y34, Z-2. Рабочий угол 0..90 градусов.',
 'Новые покупные узлы пока не имеют подтверждённой присадки. Их отверстия НЕ выдуманы в DXF.',
 'Сверления корпуса и контуры показаны для проверки. Для полного заказа этого комплекта недостаточно.'])
for h in model['holds']:text(35,390-model['holds'].index(h)*28,h,11)
new('Нижний отсек: последовательность без телескопического ящика')
lines(['1. Потянуть за прорезь фасада. Опустить на 90 градусов, удерживая рукой; не бросать вниз.',
 '2. Петля 500 мм вдоль нижней кромки; два ограничителя хода, один магнитный фиксатор закрытия.',
 '3. Приподнять площадку на 10 мм, вытащить на 430 мм вперёд; затем поставить на пол.',
 '4. На площадке нет боковин ящика. Нажимать педаль только на полу, не на открытом фасаде.',
 '5. В обратном порядке вернуть площадку, уложить кабель и поднять фасад. Кабель не зажимать петлёй.',
 'Проверка кинематики: 91 положение дверцы. Минимум до пола 18 мм; дверца остаётся перед корпусом.',
 'При вынимании: низ ножек Y42, верх открытого фасада Y34 - зазор 8 мм.',
 'Верх AIRSTEP при подъёме Y119; низ переднего ребра Y140 - зазор 21 мм.',
 'Показанная ось требует соответствующей установки петли. Сначала примерить петлю к образцу ЛДСП 16.',
 'Шаблон отверстий, тип ограничителей и их длина - HOLD. Этот лист не задаёт ложную заводскую присадку.'])
# Side-view sequence, identical coordinates to viewer (X omitted).
for i,(title,angle,offset) in enumerate([('Закрыто',0,(0,0)),('Фасад вниз',90,(0,0)),('Площадка вынута',90,(-430,10))]):
 ox=60+i*370;oy=130;s=.42;text(ox,390,title,14)
 def rect(z,y,w,h):c.rect(ox+(z+450)*s,oy+y*s,w*s,h*s)
 c.setStrokeColorRGB(.2,.3,.3);rect(0,16,360,16);rect(0,140,16,80)
 a=math.radians(angle);pts=[]
 for y,z in [(36,-18),(136,-18),(136,-2),(36,-2)]:pts.append((ox+(-2-(y-34)*math.sin(a)+(z+2)*math.cos(a)+450)*s,oy+(34+(y-34)*math.cos(a)+(z+2)*math.sin(a))*s))
 path=c.beginPath();path.moveTo(*pts[0])
 for pt in pts[1:]:path.lineTo(*pt)
 path.close();c.drawPath(path);rect(65+offset[0],48+offset[1],220,16)
new('Гитара: принцип оригинала, без деревянной вилки')
lines(['Две нижние мягкие консоли: опорные оси Y100, Z110 и Z285, вылет 120 мм от боковины X654.',
 'Верхний мягкий ограничитель: ось Y760, Z180, вылет 115 мм; две мягкие ограничительные шайбы.',
 'Форма воспроизведена по крупным фото производителя, а не по чужому рисунку.',
 'Производитель не указал марку пластика: утверждать, что это именно полиэтилен, нельзя.',
 'Выбранного покупного аналога с чертежом крепления пока нет. Резерв на три держателя 1000 ₽.',
 'Не заменять нижние опоры обычными крючками за гриф: другая нагрузка и другая геометрия.',
 'Рекомендуемая схема крепления к ЛДСП: сквозной болт с широкой шайбой/ответной пластиной,',
 'а не длинный шуруп в 16-мм плиту. Диаметр и присадка - только по выбранному держателю.',
 'Расчётное требование при 5 кг и плече 90 мм: до 4,42 Нм на одну нижнюю опору при неравномерности.',
 'Гриф только ограничивается от выпадения. Две нижние опоры несут массу; нужен удерживающий ремешок.',
 'Контактные накладки должны быть совместимы с лаком гитары. Никакой бытовой резины с неизвестным составом.',
 'Примерка и проба эквивалентом груза обязательны до использования настоящей гитары.'])
c.linkURL('https://on-stage.com/images/products/98739/48143/800x800/TMP-GWS5000RB.jpg',(35,350,500,370));text(35,357,'Фото верхнего ограничителя On-Stage (ссылка)',11)
c.linkURL('https://on-stage.com/images/products/98739/48144/800x800/TMP-GWS5000RB.jpg',(35,320,500,340));text(35,327,'Фото нижней мягкой опоры On-Stage (ссылка)',11)
new('Устойчивость и ограничения нагрузки')
lines(['Опоры пола X0..654, Z20..340. Плотность ЛДСП принята 600 кг/м³; масса фурнитуры не учитывается.',
 'Скрининговый расчёт, не сертификация: Fкр = восстанавливающий момент / 0,8 м.',
 'Без Katana устойчивость против толчка 50 Н сверху не обеспечена. Страховка обязательна.',
 'Полка K: одна вертикальная балка 16x80 с пролётом 622 несёт 20 кг по консервативной схеме.',
 f"Напряжение {calc['shelf']['stress_MPa']} МПа; условный длительный прогиб {calc['shelf']['long_deflection_mm']} мм.",
 'Для фактической плиты нужно подтвердить E>=1600 МПа и прочность изгиба >=11 МПа.',
 'Педалборд: расчётное усилие нажатия 300 Н, только на полу. Это не ступенька.',
 'Ручки: переносить пустой корпус вдвоём, не стойку с усилителем и гитарой. Прочность вырезов не испытана.'])
text(35,455,'Katana / гитара / дверца / площадка на полу       Масса, кг       Fкр вперёд / вправо, Н',11)
for i,(k,v) in enumerate(calc['cases'].items()):text(35,427-i*25,f"{k}       {v['mass_kg']}       {v['critical_force_at_800_N']['front']} / {v['critical_force_at_800_N']['right']}",11)
new('Смета: поштучно и на вес, без лишних упаковок')
lines([f'Фурнитура с явно указанными резервами: {subtotal:.2f} ₽. Общий предварительный бюджет: {total:.2f} ₽.',
 'Доставка и монтаж к стене не включены; это не котировка цеха и не окончательная цена изделия.',
 'Крепика: 34 конфирмата x 1,98 = 67,32 ₽; 20 саморезов x ~0,002 кг x 1273,96 = ~50,96 ₽.',
 'Сумма весовых позиций ориентировочная: масса в карточке округлена, оплату определят весы магазина.',
 'Шайбы DIN 9021 М10: 3,74 ₽/шт.; фасадные дюбели тоже есть поштучно. Упаковка не нужна.',
 'В актуальную смету не входит рулон резины, большие пачки саморезов или направляющие ящика.',
 'Точные ссылки, суммы по позициям и различие цены/резерва - в hardware.html.'])
for i,(name,q,price,url,note) in enumerate(rows):
 y=495-i*32;text(35,y,name,11);text(700,y,q,10);text(1000,y,f'{price:.2f} ₽',11)
 if url:c.linkURL(url,(35,y-3,680,y+13))
for p in P:
 for start in range(0,max(1,len(p['holes'])),18):
  new(f"{p['id']} / {p['name']} / {p['w']} x {p['h']} x 16")
  scale=min(420/p['w'],500/p['h']);ox=55;oy=160
  c.setStrokeColorRGB(.2,.3,.3);c.rect(ox,oy,p['w']*scale,p['h']*scale)
  for s in p['slots']:
   w,h=(s['length'],s['width']) if s['axis']=='u' else (s['width'],s['length'])
   c.roundRect(ox+(s['x']-w/2)*scale,oy+(s['y']-h/2)*scale,w*scale,h*scale,s['width']*scale/2)
  for h in p['holes']:
   x,y,n=h['local'];c.circle(ox+x*scale,oy+y*scale,max(1.5,h['diam']*scale/2));text(ox+x*scale+2,oy+y*scale+3,h['id'],6)
  text(535,714,'ID       u        v        n       Ø      глубина      направление',11)
  for i,h in enumerate(p['holes'][start:start+18]):
   vals=[h['id'],*h['local'],h['diam'],h['depth'],str(h['dir'])]
   for x,val in zip([535,620,690,760,825,880,980],vals):text(x,685-i*24,val,10)
  for i,s in enumerate(p['slots']):text(535,190-i*23,f"Паз: центр ({s['x']}; {s['y']}), {s['length']}x{s['width']}, R{s['width']/2}",11)
  text(35,110,'u вправо, v вверх. n - толщина. Начало в чистовом углу детали; направления в таблице локальные.',11)
  text(35,87,'Покупная фурнитура: присадка HOLD. Контур после кромки 0,4 мм; распил прямоугольника -0,8 мм по обеим осям.',10)
  text(35,65,'Отверстия конфирмата в головной детали: фаска Ø10 x 1,5; сверить с фактической головкой до серии.',10)
c.save();print(json.dumps(dict(checks=checks,pdf_pages=number,hardware_budget=subtotal,total_budget=total),ensure_ascii=False))
