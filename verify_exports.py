"""Independent roundtrip checks of exported vertices, quantities and assembly."""
import json, math, xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
R=Path(__file__).resolve().parent
m=json.loads((R/'output/model.json').read_text())
def entities(path):
 lines=path.read_text().splitlines(); pairs=list(zip(lines[::2],lines[1::2])); out={}; layer=None; pts=[]; x=None
 for code,value in pairs:
  if code=='0':
   if layer and pts: out[layer]=pts
   layer=None;pts=[]
  elif code=='8':layer=value
  elif code=='10': x=float(value)
  elif code=='20': pts.append([x,float(value)])
 return out
for key,v in m['variants'].items():
 suffix='' if key=='flow' else '_'+key
 cad=entities(R/f'output/guitar_stand_layout_2440x1220{suffix}.dxf')
 svg=ET.parse(R/f'output/guitar_stand_layout_2440x1220{suffix}.svg').getroot()
 sp={p.attrib['data-id']:[[float(q.split(',')[0]),1220-float(q.split(',')[1])] for q in p.attrib['points'].split()] for p in svg.findall('{http://www.w3.org/2000/svg}polygon')}
 assert len(cad)==15 and len(sp)==14
 for item in v['layout']:
  for output in [cad['CUT_'+item['id']],sp[item['id']]]:
   assert len(output)==len(item['poly'])
   assert max(math.dist(a,b) for a,b in zip(output,item['poly']))<.000002
 assert len(PdfReader(R/f'output/guitar_stand_drawings{suffix}.pdf').pages)==4
 assert len([i for i in v['layout'] if i['code']=='B'])==4
 for code in ['T','K','A','N','U']:assert len([i for i in v['layout'] if i['code']==code])==2
print('PASS: 3 variants; DXF/SVG match model.json within 0.000002 mm; 14 parts each; 4 PDF pages each.')
parts={p['id']:p for p in m['parts']}
assert m['sideHeight']+m['thickness']==m['envelope'][1]
assert parts['A']['size'][1]>parts['K']['size'][1]>parts['T']['size'][1]
amp=m['equipment']['amp']; tilt=math.radians(amp['rotation'][0]); dy=amp['pos'][1]-251;dz=amp['pos'][2]-230
assert abs(dy*math.cos(tilt)+dz*math.sin(tilt)-208)<1e-6
a=math.radians(10); n_top=parts['N']['pos'][1]+45
a_bottom_at_n=90+(400-210)*math.tan(a)-9/math.cos(a)
assert a_bottom_at_n>n_top
print(f'PASS: base deepest; 782+18=800; amp rests on K; N/A rear clearance >= {a_bottom_at_n-n_top:.2f} mm.')
ped=m['equipment']['pedal']; switch_y=ped['pos'][1]+26*math.cos(a); switch_z=45-26*math.sin(a)
lower_k_at_switch=251-(switch_z-230)*math.tan(tilt)-9/math.cos(tilt)
top_amp=amp['pos'][1]+199*math.cos(tilt)+119*abs(math.sin(tilt))
print(f'ERGONOMICS (not human-fit approval): button Y={switch_y:.1f}, K plane clearance={lower_k_at_switch-switch_y:.1f}, amp nominal overhead={782-top_amp:.1f} mm.')
