"""D2 millimetres. Mechanical prototype; calculated, not physically tested."""
import math
P=[]; J=[]
X=[1,0,0];Y=[0,1,0];Z=[0,0,1]
def add(a,b):return [x+y for x,y in zip(a,b)]
def mul(a,s):return [x*s for x in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def part(id,name,w,h,origin,u,v,n,group='frame',t=16):
 p=dict(id=id,name=name,w=w,h=h,t=t,origin=origin,u=u,v=v,n=n,group=group,holes=[],slots=[])
 P.append(p);return p
def hole(p,start,direction,diam,depth,job,joint='',cs=0):
 delta=[start[i]-p['origin'][i] for i in range(3)]
 loc=[round(dot(delta,p[k]),4) for k in ['u','v','n']]
 dr=[dot(direction,p[k]) for k in ['u','v','n']]; ext=[p['w'],p['h'],p['t']]
 axis=next(i for i,x in enumerate(dr) if x)
 assert sum(abs(x) for x in dr)==1
 assert abs(loc[axis]-(0 if dr[axis]>0 else ext[axis]))<.001,(p['id'],loc,dr)
 assert depth<=ext[axis]
 for i in range(3):
  if i!=axis:assert diam/2<=loc[i]<=ext[i]-diam/2,(p['id'],loc)
 rec=dict(id=f"{p['id']}.{len(p['holes'])+1:02}",local=loc,dir=dr,world=start,worldDir=direction,diam=diam,depth=depth,job=job,joint=joint,cs=cs)
 p['holes'].append(rec);return rec
def joint(head,mate,start,direction,kind='C7'):
 id=f'J{len(J)+1:02}'; end=add(start,mul(direction,16))
 dia,dep=(7,38) if kind=='C7' else (4.5,12)
 hole(head,start,direction,dia,16,'сквозное',id,10 if kind=='C7' else 0)
 hole(mate,end,direction,5 if kind=='C7' else 2.5,dep,'глухое',id)
 J.append(dict(id=id,head=head['id'],mate=mate['id'],start=start,dir=direction,kind=kind))
L=part('L','Боковина левая',360,768,[0,16,0],Z,Y,X)
R=part('R','Боковина правая',360,768,[638,16,0],Z,Y,X)
T=part('T','Столешница ноутбука',654,360,[0,784,0],X,Z,Y)
D=part('D','Дно корпуса',622,360,[16,16,0],X,Z,Y)
K=part('K','Полка Katana',622,360,[16,220,0],X,Z,Y)
KF=part('KF','Переднее ребро полки',622,80,[16,140,0],X,Y,Z)
KR=part('KR','Заднее ребро полки',622,80,[16,140,344],X,Y,Z)
V=part('V','Нижняя задняя связь',622,80,[16,242,344],X,Y,Z)
U=part('U','Верхняя задняя связь',622,80,[16,680,344],X,Y,Z)
# Two rigid spacers keep the carcass 48 mm from a sound concrete wall.
for x in [100,554]:
 hole(U,[x,720,344],Z,11,16,'W1 SXRL 10x160 FUS; шайба DIN9021 M10')
 for k in range(3):
  p=part(f'W{x}_{k+1}','Дистанционная прокладка стены',50,50,[x-25,695,360+16*k],X,Y,Z,'wall')
  hole(p,[x,720,360+16*k],Z,11,16,'W1 сквозная ось стенового крепления')
E1=part('E1','Передняя общая опора',834,50,[0,0,20],X,Z,Y)
E2=part('E2','Задняя общая опора',834,50,[0,0,290],X,Z,Y)
# Guitars stand on the lower supports; the upper fork is a lateral restraint.
GB=part('GB','Основание гитары',180,360,[654,16,0],X,Z,Y,'guitar')
G1=part('G1','Мягкая опора корпуса 1',160,50,[664,32,105],X,Z,Y,'guitar')
G2=part('G2','Мягкая опора корпуса 2',160,50,[664,32,205],X,Z,Y,'guitar')
GN=part('GN','Вилка грифа',160,160,[654,650,100],X,Z,Y,'guitar')
GN['notch']=dict(start=85,center=80,radius=33) # opens at u=w
GN['slots']=[dict(x=120,y=y,length=22,width=5,axis='v') for y in [20,140]]
GC1=part('GC1','Ребро вилки переднее',160,100,[654,550,100],X,Y,Z,'guitar')
GC2=part('GC2','Ребро вилки заднее',160,100,[654,550,244],X,Y,Z,'guitar')
# 622 - 2*12.7 = 596.6 outside drawer width, manufacturer's side clearance.
QL=part('QL','Бок ящика левый',300,90,[28.7,42,32],Z,Y,X,'drawer')
QR=part('QR','Бок ящика правый',300,90,[609.3,42,32],Z,Y,X,'drawer')
QB=part('QB','Дно ящика',564.6,300,[44.7,42,32],X,Z,Y,'drawer')
F=part('F','Фасад ящика',618,100,[18,36,16],X,Y,Z,'drawer')
F['slots']=[dict(x=309,y=72,length=110,width=24,axis='u')]
PB=part('PB','Съёмная площадка AIRSTEP',500,220,[77,74,65],X,Z,Y,'pedal')
PF1=part('PF1','Опора педалборда 1',500,35,[77,58,70],X,Z,Y,'pedal')
PF2=part('PF2','Опора педалборда 2',500,35,[77,58,245],X,Z,Y,'pedal')
PB['slots']=[dict(x=250,y=150,length=130,width=18,axis='u')]
for side,x,dx in [(L,0,1),(R,654,-1)]:
 for shelf,cy in [(D,24),(K,228)]:
  for z in [50,180,310]:joint(side,shelf,[x,cy,z],[dx,0,0])
 for rear in [V,U]:
  for yy in [20,60]:joint(side,rear,[x,rear['origin'][1]+yy,352],[dx,0,0])
 for rib,z in [(KF,8),(KR,352)]:
  for yy in [155,205]:joint(side,rib,[x,yy,z],[dx,0,0])
for rib,z in [(KF,8),(KR,352)]:
 for x in [100,250,400,550]:joint(K,rib,[x,236,z],[0,-1,0],'S4')
for side,x in [(L,8),(R,646)]:
 for z in [50,180,310]:joint(T,side,[x,800,z],[0,-1,0])
for rail,z in [(E1,45),(E2,315)]:
 for x in [70,327,584]:joint(D,rail,[x,32,z],[0,-1,0],'S4')
 for x in [700,790]:joint(GB,rail,[x,32,z],[0,-1,0],'S4')
for pad,z in [(G1,130),(G2,230)]:
 for x in [700,790]:joint(GB,pad,[x,16,z],Y,'S4')
for gusset,z in [(GC1,108),(GC2,252)]:
 for y in [578,622]:joint(R,gusset,[638,y,z],X)
 for x in [710,790]:joint(GN,gusset,[x,666,z],[0,-1,0])
for side,x,dx in [(QL,28.7,1),(QR,625.3,-1)]:
 for z in [75,175,285]:joint(side,QB,[x,50,z],[dx,0,0])
for side,x in [(QL,36.7),(QR,617.3)]:
 for y in [64,114]:joint(F,side,[x,y,16],Z)
for foot,z in [(PF1,87.5),(PF2,262.5)]:
 for x in [127,327,527]:joint(PB,foot,[x,90,z],[0,-1,0],'S4')
# Reference DB4501 drawing (2014): cabinet 32,171.5 from guide front;
# drawer centres 72,200,264 from drawer front for NL300. Slotted fixing holes
# allow setting; supplier sample template check is explicitly a release gate.
for side,x,dx in [(L,16,-1),(R,638,1)]:
 for z in [64,203.5]:hole(side,[x,92,z],[dx,0,0],2.5,12,'S16 направляющая корпуса; шаблон DB4501')
for side,x,dx in [(QL,28.7,1),(QR,625.3,-1)]:
 for z in [104,232,296]:hole(side,[x,92,z],[dx,0,0],2.5,12,'S16 направляющая ящика; шаблон DB4501')
equipment=[dict(id='amp',name='Katana-50 MkII',size=[470,398,238],pos=[92,236,45],mass=11.6),dict(id='pedal',name='AIRSTEP Kat Edition',size=[300,45,70],pos=[177,90,95],mass=.65),dict(id='laptop',name='MacBook Air 15',size=[340.4,11.5,237.6],pos=[156.8,800,50],mass=1.51)]
def calculations():
 # 600 kg/m3 conservative dead mass for tipping; actual supplied board must be weighed.
 masses=[]
 for p in P:
  area=p['w']*p['h']
  if p.get('notch'):area-=((p['w']-85)*66+math.pi*33**2/2)
  for s in p['slots']:area-=s['width']*(s['length']-s['width'])+math.pi*s['width']**2/4
  mass=area*p['t']*600/1e9
  center=add(p['origin'],add(mul(p['u'],p['w']/2),add(mul(p['v'],p['h']/2),mul(p['n'],p['t']/2))))
  masses.append(dict(id=p['id'],mass=mass,center=center,group=p['group']))
 def state(amp=True,drawer=False,guitar=True,accessories=True):
  items=[dict(m) for m in masses]
  for m in items:
   m['center']=m['center'][:]
   if drawer and m['group'] in ('drawer','pedal'):m['center'][2]-=300
  for e in equipment:
   if e['id']=='amp' and not amp:continue
   if e['id']!='amp' and not accessories:continue
   pos=[e['pos'][i]+e['size'][i]/2 for i in range(3)]
   if drawer and e['id']=='pedal':pos[2]-=300
   items.append(dict(mass=e['mass'],center=pos))
  if guitar:items.append(dict(mass=5,center=[744,490,180]))
  total=sum(m['mass'] for m in items);cg=[sum(m['mass']*m['center'][i] for m in items)/total for i in range(3)]
  moments=dict(front=sum(m['mass']*9.81*(m['center'][2]-20)/1000 for m in items),rear=sum(m['mass']*9.81*(340-m['center'][2])/1000 for m in items),left=sum(m['mass']*9.81*m['center'][0]/1000 for m in items),right=sum(m['mass']*9.81*(834-m['center'][0])/1000 for m in items))
  return dict(mass_kg=round(total,2),cg_mm=[round(v,1) for v in cg],restoring_Nm={k:round(v,2) for k,v in moments.items()},critical_horizontal_force_at_800_N={k:round(v/.8,1) for k,v in moments.items()},drawer_pull_30N_at_92mm_margin=round(moments['front']/(30*.092),2))
 # P2 datasheet: E>=1600 MPa, bending>=11 MPa; criterion static stress<=11/3.
 # Conservative uncomposite 16 mm shelf, two concentrated feet lines at a=76 mm.
 E=1600;span=622;b=16;t=80;I=b*t**3/12;load=20*9.81
 sigma=(load*span/4)/(b*t*t/6);deflection=load*span**3/(48*E*I)
 # Independent floor pedalboard across the 140 mm clear spacing of its foot strips.
 pp=300;pl=140;pb=70;pi=pb*16**3/12;pedal_E=1600
 cases={f'amp_{a}_drawer_{d}_guitar_{g}':state(a,d,g) for a in [False,True] for d in [False,True] for g in [False,True]}
 cases.update(empty_closed=state(False,False,False,False),empty_open=state(False,True,False,False))
 return dict(assumptions=dict(board_density_kg_m3=600,E16_MPa=1600,bending16_MPa=11,material_safety_factor=3,amp_design_kg=20,guitar_max_kg=5,pedal_press_N=300,guitar_lateral_N=30,drawer_payload_limit_kg=3),cases=cases,shelf=dict(model='One 16x80 vertical rib, span 622, entire 20 kg central load; second rib ignored conservatively; no composite action assumed',stress_MPa=round(sigma,3),allowable_MPa=round(11/3,3),short_deflection_mm=round(deflection,3),creep_multiplier_assumed=3,long_deflection_mm=round(deflection*3,3),deflection_limit_mm=round(span/200,3)),pedalboard=dict(stress_MPa=round((pp*pl/4)/(pb*16**2/6),3),deflection_mm=round(pp*pl**3/(48*pedal_E*pi),3)),drawer=dict(slide_rated_kg=15,estimated_wood_and_pedal_kg=round(sum(m['mass'] for m in masses if m['group'] in ('drawer','pedal'))+.65,2),foot_press_allowed=False),panel_between_ribs=dict(span_mm=328,load_kg=20,width_mm=470,stress_MPa=round(196.2*328/4/(470*16**2/6),3),short_deflection_mm=round(196.2*328**3/(48*1600*(470*16**3/12)),3)),guitar_fork=dict(lateral_force_N=30,lever_mm=160,moment_Nmm=4800,root_screw_pair_arm_mm=44,tension_per_upper_screw_N=round(4800/44/2,1),conservative_one_prong_stress_MPa=round(30*75/(32*16**2/6),3),test_force_N=60),wall=dict(type='fischer SXRL 10x160 FUS 522724',quantity=2,substrate='sound C20/25 concrete only; not plasterboard or hollow masonry',spacer_mm=48,board_mm=16,washer_mm=2.5,embedment_mm=93.5,drill_diameter_mm=10,drill_depth_from_washer_face_mm=170,design_horizontal_load_N=200,tie_force_total_N=round(200*.8/.72,1),proof_force_total_N=300,capacity_verified=False),limits=['Screening calculations, not a furniture standard test or certification.','Fastener withdrawal and joint rotational stiffness require first-article proof tests.','Wall fixing is mandatory; calculated demand is not a measured connection capacity.','Ventilation deferred by owner.'])
calc=calculations()
model=dict(revision='D2',units='mm',envelope=[654,800,360],footprint=[834,360],parts=P,joints=J,equipment=equipment,calculations=calc,mechanism=dict(type='BOYARD DB4501Zn/300',travel=300,clearance_each=12.7,axis_y=92,guide_front_z=32,pedal_floor_delta=[0,-58,-650]),guitar=dict(type='bottom-supported cradle with padded neck fork',max_mass=5,body_envelope=[60,460,340],neck_width_max=60,reference='Ibanez RG family envelope, not measured RG421'))
