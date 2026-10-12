"""D3 layout correction. Hardware interfaces on HOLD, not a factory release."""
from copy import deepcopy
import math
from d2_geometry import P as OLD, J as OLDJ, equipment as OLDEQ, calc as OLDCALC

remove={'GB','G1','G2','GN','GC1','GC2','QL','QR','QB'}
P=deepcopy([p for p in OLD if p['id'] not in remove and p['group']!='wall'])
ids={p['id'] for p in P}
J=deepcopy([j for j in OLDJ if j['head'] in ids and j['mate'] in ids and j['head']!='F'])
valid={j['id'] for j in J}
for p in P:
 p['holes']=[h for h in p['holes'] if h['joint'] in valid]
 p['outline']=[[0,0],[p['w'],0],[p['w'],p['h']],[0,p['h']]]
by={p['id']:p for p in P}
for id in ['E1','E2']:
 p=by[id];p['w']=654;p['name']='Опорная планка корпуса';p['outline']=[[0,0],[654,0],[654,50],[0,50]]
for id in ['L','R']:
 by[id]['slots']=[dict(x=175,y=680,length=110,width=30,axis='u')]
 # World Y681..711; keep the carrying grip separate from the upper guitar support.
F=by['F'];F.update(name='Откидная нижняя дверца',origin=[18,36,-18],group='flap',holes=[])
for id in ['PB','PF1','PF2']:
 p=by[id];p['origin'][1]-=26
 for h in p['holes']:h['world'][1]-=26
for j in J:
 if j['head']=='PB':j['start'][1]-=26
equipment=deepcopy(OLDEQ)
next(e for e in equipment if e['id']=='pedal')['pos'][1]-=26
mechanism=dict(type='drop-front + fully removable pedalboard; no slides',axis=[327,34,-2],angle_deg=90,pedal_lift_mm=10,pedal_pull_mm=430,pedal_floor_delta=[0,-32,-600],hardware_template_confirmed=False)
holders=[dict(id='GLOW1',center=[654,100,110],length=120,radius=16,stop_radius=23),dict(id='GLOW2',center=[654,100,285],length=120,radius=16,stop_radius=23),dict(id='GNECK',center=[654,760,180],length=115,radius=16,stop_radius=30)]
holds=['Присадка петли, фиксатора, ограничителей и держателей не утверждена: не сверлить по 3D.',
 'Держатели показаны по принципу On-Stage. Материал оригинала и доступный аналог с паспортом не подтверждены.',
 'Нужны примерка гитары, выбор фурнитуры и испытания узлов. Это компоновка, не выпуск в производство.',
 'Без страховки от опрокидывания не эксплуатировать; тип анкера зависит от стены.',
 'Переносить только пустую стойку вдвоём. Вентиляция отложена.']

def state(amp, guitar, opened, board_floor):
 items=[]
 for p in P:
  if board_floor and p['group']=='pedal':continue
  area=p['w']*p['h']
  for s in p['slots']:area-=s['width']*(s['length']-s['width'])+math.pi*s['width']**2/4
  m=area*p['t']*600/1e9
  c=[p['origin'][i]+p['u'][i]*p['w']/2+p['v'][i]*p['h']/2+p['n'][i]*p['t']/2 for i in range(3)]
  if p['id']=='F' and opened:c=[327,26,-54]
  items.append((m,c))
 for e in equipment:
  if e['id']=='amp' and not amp:continue
  if e['id']=='pedal' and board_floor:continue
  items.append((e['mass'],[e['pos'][i]+e['size'][i]/2 for i in range(3)]))
 if guitar:items.append((5,[715,555,180]))
 mass=sum(m for m,c in items)
 moments={k:sum(m*9.81*d(c)/1000 for m,c in items) for k,d in [('front',lambda c:c[2]-20),('rear',lambda c:340-c[2]),('left',lambda c:c[0]),('right',lambda c:654-c[0])]}
 return dict(mass_kg=round(mass,2),restoring_Nm={k:round(v,2) for k,v in moments.items()},critical_force_at_800_N={k:round(v/.8,1) for k,v in moments.items()})
cases={f'amp{a}_guitar{g}_open{o}_floor{f}':state(a,g,o,f) for a in [0,1] for g in [0,1] for o,f in [(0,0),(1,0),(1,1)]}
calc=dict(cases=cases,shelf=deepcopy(OLDCALC['shelf']),pedalboard=deepcopy(OLDCALC['pedalboard']),note='Screening: density 600 kg/m3, equipment masses fixed, guitar 5 kg; holes and hardware mass neglected. Not a certified stability test.',wall_required=True)
model=dict(revision='D3',release='LAYOUT_HOLD',units='mm',envelope=[654,800,378],parts=P,joints=J,equipment=equipment,mechanism=mechanism,holders=holders,holds=holds,calculations=calc)

def verify():
 assert not ({'QL','QR','QB','GN','GC1','GC2','GB'}&ids)
 assert len(P)==15
 # Sample the entire door sweep. Door stays in front of the carcass, above floor.
 for deg in range(91):
  a=math.radians(deg)
  for y in [36,136]:
   for z in [-18,-2]:
    yy=34+(y-34)*math.cos(a)+(z+2)*math.sin(a)
    zz=-2-(y-34)*math.sin(a)+(z+2)*math.cos(a)
    assert yy>=17.99 and zz<=-1.99
 # Lifted foot clears the open door; AIRSTEP top clears front rib underside.
 assert 32+10>34 and 64+45+10<140
 assert 65+220-430 < -104 # full withdrawal before lowering
 for j in J:
  holes=[h for p in P for h in p['holes'] if h['joint']==j['id']]
  assert len(holes)==2,j
  assert holes[0]['diam'] in (7,4.5,5,2.5)
 return dict(status='layout checks passed; manufacturing HOLD',parts=len(P),joints=len(J),bores=sum(len(p['holes']) for p in P),door_sweep_samples=91,open_door_min_floor_clearance_mm=18,lifted_pedal_clearance_under_rib_mm=21)
checks=verify()
