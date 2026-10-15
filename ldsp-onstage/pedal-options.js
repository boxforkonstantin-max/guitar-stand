import * as T from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const $=id=>document.getElementById(id),host=$('view');
try {
const res=await fetch('output-d3/model.json');if(!res.ok)throw Error(`Геометрия: HTTP ${res.status}`);const data=await res.json();
const scene=new T.Scene();scene.background=new T.Color('#e4e9e8');
const camera=new T.PerspectiveCamera(38,1,1,6000),renderer=new T.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.append(renderer.domElement);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;
scene.add(new T.HemisphereLight(0xffffff,0x66757a,2.5));const light=new T.DirectionalLight(0xffffff,3);light.position.set(-600,1300,-600);scene.add(light);
const grid=new T.GridHelper(2000,20,0x87999a,0xbfcacb);grid.position.set(327,-.5,0);scene.add(grid);
const mat=c=>new T.MeshStandardMaterial({color:c,roughness:.7});const wood=mat('#a57f57'),dark=mat('#252d31'),silver=mat('#c3cacf'),green=mat('#347765'),blue=mat('#237aaf');
function box(w,h,d,x,y,z,m,parent=scene){const o=new T.Mesh(new T.BoxGeometry(w,h,d),m);o.position.set(x+w/2,y+h/2,z+d/2);parent.add(o);const edges=new T.LineSegments(new T.EdgesGeometry(o.geometry),new T.LineBasicMaterial({color:0x34444a,transparent:true,opacity:.35}));o.add(edges);return o;}
const cabinet=new T.Group();scene.add(cabinet);let left;
for(const p of data.parts){if(['F','PB','PF1','PF2','KF'].includes(p.id))continue;const sh=new T.Shape();p.outline.forEach(([x,y],i)=>i?sh.lineTo(x,y):sh.moveTo(x,y));sh.closePath();for(const s of p.slots){const path=new T.Path(),r=s.width/2,d=(s.length-s.width)/2;path.absarc(s.x+d,s.y,r,-Math.PI/2,Math.PI/2);path.absarc(s.x-d,s.y,r,Math.PI/2,Math.PI*1.5);sh.holes.push(path);}const geo=new T.ExtrudeGeometry(sh,{depth:p.t,bevelEnabled:false});const basis=new T.Matrix4().makeBasis(new T.Vector3(...p.u),new T.Vector3(...p.v),new T.Vector3(...p.n));basis.setPosition(...p.origin);geo.applyMatrix4(basis);const mesh=new T.Mesh(geo,wood);cabinet.add(mesh);if(p.id==='L')left=mesh;}
box(470,390,238,92,236,45,dark);box(438,340,4,108,250,41,mat('#495257'));for(let i=0;i<9;i++)box(9,8,9,135+i*35,626,237,silver);
box(340.4,11.5,237.6,156.8,800,50,silver);box(340.4,210,8,156.8,811.5,280,dark);
const mechanism=new T.Group();scene.add(mechanism);let door,board,beam,variant=3,amount=1,cable,clipGroup;
function pedal(parent,x,y,z){box(300,39,70,x,y,z,dark,parent);for(let i=0;i<5;i++){const b=new T.Mesh(new T.CylinderGeometry(6,6,6,16),silver);b.position.set(x+30+i*60,y+42,z+30);parent.add(b);}for(const dx of [10,270])box(20,2,70,x+dx,y-2,z,blue,parent);}
function clear(g){for(const child of [...g.children]){child.traverse(o=>{if(o.geometry)o.geometry.dispose();});g.remove(child);}}
function build(){clear(mechanism);door=new T.Group();door.position.set(0,34,-2);mechanism.add(door);board=new T.Group();mechanism.add(board);
if(variant===3){
 box(618,180,16,18,0,-16,wood,door);
 // Outside-face runners become ground supports after the 90-degree rotation.
 for(const x of [200,410])box(38,150,18,x,20,-34,green,door);
 // Pedal frame: its +Y face is +Z while closed and +Y while open.
 const fixed=new T.Group();fixed.rotation.x=Math.PI/2;fixed.position.set(0,150,2);door.add(fixed);pedal(fixed,177,0,0);
 // Short retention loops supplement hook-and-loop without covering switches.
 for(const x of [185,459])box(8,72,2,x,79,42,blue,door);
 beam=box(622,80,16,16,140,90,wood,mechanism);
}else{
 box(618,100,16,18,2,-16,wood,door);beam=box(622,80,16,16,140,0,wood,mechanism);
 box(500,16,220,77,48,65,wood,board);for(const z of [70,245])box(500,16,35,77,32,z,green,board);pedal(board,177,66,95);
}
box(500,3,5,77,32,-4,silver,mechanism);clipGroup=new T.Group();mechanism.add(clipGroup);update();}
function update(){const p=amount;
if(variant===3){door.rotation.x=-p*Math.PI/2;board.position.set(0,0,0);}else{
 door.rotation.x=-Math.min(p/.25,1)*Math.PI/2;
 const f=Math.max(0,(p-.25)/.75),points=[[0,0,0],[0,10,0],[0,10,-430],[0,-32,-600]],i=Math.min(2,Math.floor(f*3)),u=f===1?1:f*3-i;
 board.position.fromArray(points[i]).lerp(new T.Vector3(...points[i+1]),u);
}
scene.updateMatrixWorld(true);if(cable){mechanism.remove(cable);cable.geometry.dispose();cable.material.dispose();}clear(clipGroup);
// Cable is routed beside the pedal, above the hinge, with an interior service loop.
// Illustrative slack geometry, not a constant-length cable simulation or a port template.
const start=variant===3?door.localToWorld(new T.Vector3(177,155,25)):new T.Vector3(177,90,170).add(board.position);
const moving=variant===3?door.localToWorld(new T.Vector3(70,155,25)):new T.Vector3(70,90,170).add(board.position);
const path=new T.CatmullRomCurve3([start,moving,new T.Vector3(55,95,45),new T.Vector3(55,85,155),new T.Vector3(70,100,220)],false,'centripetal');
cable=new T.Mesh(new T.TubeGeometry(path,100,2.5,8,false),mat('#ec8c23'));mechanism.add(cable);for(const v of [moving,new T.Vector3(70,100,220)])box(12,10,10,v.x-6,v.y-5,v.z-5,blue,clipGroup);
cable.visible=clipGroup.visible=$('cables').checked;left.visible=!$('cutaway').checked;
$('percent').textContent=`${Math.round(p*100)}%`;$('play').textContent=p>.5?'Показать закрытие':'Показать открытие';
$('note').textContent=variant===3?'3 · Одна операция: крышка с педалью опускается на 90°. Две зелёные опоры доходят до пола. Крышка 618 × 180 × 16 мм; передняя царга перенесена внутрь на 90 мм. Липучка плюс страховочные петли.':'1 · Сначала опускается отдельная дверца. Затем площадку приподнимают на 10 мм, вынимают и ставят на пол. Педаль остаётся на липучке; положение площадки не ограничено дверцей.';
$('status').textContent=p===1?'Игровое положение · опоры на отметке пола 0 мм':p===0?'Закрыто · педаль внутри корпуса':'Промежуточное положение · не нажимать ногой';}
function view(detail=false,side=false){camera.position.set(...(side?[-1250,250,-80]:detail?[-750,570,-1000]:[-1200,1050,-1700]));orbit.target.set(327,detail||side?130:430,detail||side?-80:0);orbit.update();}
let animation=0;$('variant').onchange=()=>{cancelAnimationFrame(animation);variant=Number($('variant').value);build();};$('progress').oninput=()=>{cancelAnimationFrame(animation);amount=Number($('progress').value)/100;update();};
$('play').onclick=()=>{cancelAnimationFrame(animation);const from=amount,to=amount>.5?0:1,begin=performance.now(),duration=matchMedia('(prefers-reduced-motion: reduce)').matches?0:2400;function tick(t){const f=duration?Math.min(1,(t-begin)/duration):1;amount=from+(to-from)*(f*f*(3-2*f));$('progress').value=amount*100;update();if(f<1)animation=requestAnimationFrame(tick);}animation=requestAnimationFrame(tick);};
$('iso').onclick=()=>view();$('detail').onclick=()=>view(true);$('side').onclick=()=>view(true,true);$('cutaway').onchange=update;$('cables').onchange=update;
new ResizeObserver(()=>{renderer.setSize(host.clientWidth,host.clientHeight);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();}).observe(host);
build();view(true);renderer.setAnimationLoop(()=>{orbit.update();renderer.render(scene,camera);});
}catch(e){$('status').textContent=`Не удалось открыть 3D: ${e.message}. Обновите страницу через HTTPS.`;console.error(e);}
