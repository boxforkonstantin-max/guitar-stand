"""Independent geometry, export, nesting and source-preservation checks."""
import json,math,hashlib,subprocess
from pathlib import Path
from d2_geometry import P,J,model,calc
root=Path(__file__).resolve().parent
def bounds(p):
 pts=[[p['origin'][i]+u*p['u'][i]+v*p['v'][i]+n*p['n'][i] for i in range(3)] for u in [0,p['w']] for v in [0,p['h']] for n in [0,p['t']]]
 return [(min(v[i] for v in pts),max(v[i] for v in pts)) for i in range(3)]
collisions=[]
for i,a in enumerate(P):
 for b in P[i+1:]:
  aa,bb=bounds(a),bounds(b)
  if all(min(aa[k][1],bb[k][1])-max(aa[k][0],bb[k][0])>.001 for k in range(3)):collisions.append([a['id'],b['id']])
assert not collisions,collisions
cross=[]
for p in P:
 for i,a in enumerate(p['holes']):
  for b in p['holes'][i+1:]:
   # Axis aligned segments: independent interval distance yields exact min
   # for parallel/perpendicular segments in an orthogonal panel coordinate frame.
   aa=[sorted([a['local'][k],a['local'][k]+a['dir'][k]*a['depth']]) for k in range(3)]
   bb=[sorted([b['local'][k],b['local'][k]+b['dir'][k]*b['depth']]) for k in range(3)]
   distance=math.sqrt(sum(max(0,aa[k][0]-bb[k][1],bb[k][0]-aa[k][1])**2 for k in range(3)))
   if distance<(a['diam']+b['diam'])/2-.001:cross.append([a['id'],b['id'],distance])
assert not cross,cross
for p in P:
 for s in p['slots']:
  axis=0 if s['axis']=='u' else 1;off=(s['length']-s['width'])/2
  for h in p['holes']:
   if not h['dir'][2]:continue
   delta=[abs(h['local'][0]-s['x']),abs(h['local'][1]-s['y'])];delta[axis]=max(0,delta[axis]-off)
   ligament=math.hypot(*delta)-s['width']/2-max(h['diam'],h['cs'])/2
   assert ligament>=6,(p['id'],h['id'],'slot ligament',ligament)
out=json.loads((root/'output-d2/model.json').read_text())
assert [(p['id'],p['w'],p['h'],p['t'],p['holes']) for p in P]==[(p['id'],p['w'],p['h'],p['t'],p['holes']) for p in out['parts']]
assert sum(j['kind']=='C7' for j in J)==52
assert sum(j['kind']=='S4' for j in J)==28
assert calc['shelf']['stress_MPa']<calc['shelf']['allowable_MPa']
assert calc['shelf']['long_deflection_mm']<calc['shelf']['deflection_limit_mm']
assert calc['pedalboard']['stress_MPa']<11/3
# Closed and fully open drawer fit inside their prescribed rail corridor.
for travel in range(301):
 for p in P:
  if p['group'] not in ('drawer','pedal'):continue
  bb=bounds(p);bb[2]=(bb[2][0]-travel,bb[2][1]-travel)
  assert bb[0][0]>=16 and bb[0][1]<=638 and bb[1][0]>=32 and bb[1][1]<=176
unchanged=subprocess.check_output(['git','diff','6cf5f225f86aeb8bb675772783785e8cb7b562a1','--','app','output','stand_geometry.py'],cwd=root.parent,text=True)
assert not unchanged,'R6 changed'
report=dict(wood_intersections='PASS',bore_intersections='PASS',export_dimensions='PASS',drawer_travel_0_to_300='PASS',fastener_quantities='PASS',beam_criteria='PASS',R6_unchanged='PASS',not_verified=['actual rail pattern revision','anchor load capacity and substrate','joint withdrawal physical capacity','thermal operation','actual guitar fit'])
(root/'output-d2/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
