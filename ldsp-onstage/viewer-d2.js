import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {TransformControls} from 'three/addons/controls/TransformControls.js';
const $=id=>document.getElementById(id),host=$('view');
try{
const response=await fetch('./output-d2/model.json');if(!response.ok)throw Error(`model.json: ${response.status}`);
const data=await response.json(),scene=new THREE.Scene();scene.background=new THREE.Color('#e7eceb');
const camera=new THREE.PerspectiveCamera(37,1,1,8000);camera.position.set(1700,1250,-2100);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.target.set(420,480,-80);orbit.enableDamping=true;
const transform=new TransformControls(camera,renderer.domElement);transform.setTranslationSnap(5);transform.setRotationSnap(Math.PI/36);scene.add(transform.getHelper());transform.addEventListener('dragging-changed',e=>orbit.enabled=!e.value);
scene.add(new THREE.HemisphereLight(0xffffff,0x7e8276,2.5));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(400,1300,-500);scene.add(light);
const grid=new THREE.GridHelper(2400,24,0x83989c,0xc4cfcd);grid.position.set(327,-2,180);scene.add(grid);
const material=new THREE.MeshStandardMaterial({color:0x9e7650,roughness:.83,side:THREE.DoubleSide}),groups=[],marks=[],equipment=new THREE.Group();scene.add(equipment);let trayOut=false;
function box(w,h,d,x,y,z,mat,parent=equipment){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);o.position.set(x+w/2,y+h/2,z+d/2);parent.add(o);return o;}
function label(text,x,y,z,parent){const c=document.createElement('canvas');c.width=256;c.height=80;const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,256,80);g.fillStyle='#173942';g.font='bold 36px sans-serif';g.fillText(text,12,53);const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),depthTest:false}));sp.position.set(x,y,z);sp.scale.set(78,24,1);parent.add(sp);}
function capsule(path,s){const r=s.width/2,d=(s.length-s.width)/2;if(s.axis==='u'){path.absarc(s.x+d,s.y,r,-Math.PI/2,Math.PI/2);path.absarc(s.x-d,s.y,r,Math.PI/2,Math.PI*1.5);}else{path.absarc(s.x,s.y+d,r,0,Math.PI);path.absarc(s.x,s.y-d,r,Math.PI,2*Math.PI);}path.closePath();}
for(const p of data.parts){
 const group=new THREE.Group();scene.add(group);const shape=new THREE.Shape();p.outline.forEach(([x,y],i)=>i?shape.lineTo(x,y):shape.moveTo(x,y));shape.closePath();
 for(const h of p.holes)if(h.dir[2]&&h.depth===p.t){const path=new THREE.Path();path.absarc(h.local[0],h.local[1],h.diam/2,0,Math.PI*2,true);shape.holes.push(path);}
 for(const s of p.slots){const path=new THREE.Path();capsule(path,s);shape.holes.push(path);}
 const geom=new THREE.ExtrudeGeometry(shape,{depth:p.t,bevelEnabled:false,curveSegments:20});const m=new THREE.Matrix4().makeBasis(new THREE.Vector3(...p.u),new THREE.Vector3(...p.v),new THREE.Vector3(...p.n));m.setPosition(...p.origin);geom.applyMatrix4(m);
 geom.computeBoundingBox();const pivot=geom.boundingBox.getCenter(new THREE.Vector3());geom.translate(-pivot.x,-pivot.y,-pivot.z);group.position.copy(pivot);
 const mesh=new THREE.Mesh(geom,material.clone());group.add(mesh);mesh.userData.group=group;group.add(new THREE.LineSegments(new THREE.EdgesGeometry(geom,25),new THREE.LineBasicMaterial({color:0x594532})));
 const drilling=new THREE.Group();group.add(drilling);marks.push(drilling);
 for(const h of p.holes){const start=new THREE.Vector3(...h.world),end=start.clone().addScaledVector(new THREE.Vector3(...h.worldDir),h.depth);drilling.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([start,end]),new THREE.LineBasicMaterial({color:0xc02f23,depthTest:false,transparent:true,opacity:.65})));const dot=new THREE.Mesh(new THREE.SphereGeometry(2.5,8,6),new THREE.MeshBasicMaterial({color:0xc02f23,depthTest:false}));dot.position.copy(start);drilling.add(dot);}
 drilling.position.copy(pivot).negate();group.userData={part:p,mesh,pivot};groups.push(group);const button=document.createElement('button');button.textContent=`${p.id} · ${p.name}`;button.setAttribute('aria-pressed','false');button.onclick=()=>select(group);$('parts').appendChild(button);group.userData.button=button;
}
function select(g){for(const v of groups){v.userData.button.setAttribute('aria-pressed',String(v===g));v.userData.mesh.material.color.setHex(v===g?0xd6b275:0x9e7650);}transform.attach(g);const p=g.userData.part;$('info').textContent=`${p.id} · ${p.name}\n${p.w} × ${p.h} × ${p.t} мм · ${p.holes.length} сверлений\nБазы и глубины — в PDF. Изменения здесь не меняют чертёж.`;}
const metal=new THREE.MeshStandardMaterial({color:0xb8bec1,metalness:.7,roughness:.35});
for(const j of data.joints){const dir=new THREE.Vector3(...j.dir),start=new THREE.Vector3(...j.start),len=j.kind==='C7'?50:30;const owner=groups.find(g=>g.userData.part.id===j.head);for(const [r,h,offset] of [[j.kind==='C7'?3.5:2,len,len/2],[j.kind==='C7'?5:4,1,-.5]]){const bolt=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,12),metal);bolt.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir);bolt.position.copy(start).addScaledVector(dir,offset).sub(owner.userData.pivot);owner.add(bolt);}}
const dark=new THREE.MeshStandardMaterial({color:0x202426,roughness:.9}),grille=new THREE.MeshStandardMaterial({color:0x42494a,roughness:1});
const amp=data.equipment.find(e=>e.id==='amp');box(amp.size[0],amp.size[1]-8,amp.size[2],...amp.pos,dark);box(438,340,4,108,amp.pos[1]+16,41,grille);label('BOSS',327,487,35,equipment);
// Equipment controls are schematic, not drilling coordinates.
for(let i=0;i<9;i++)box(9,8,9,135+i*35,amp.pos[1]+amp.size[1]-8,237,dark);
const pedalGroup=new THREE.Group();equipment.add(pedalGroup);const pedal=data.equipment.find(e=>e.id==='pedal');box(pedal.size[0],pedal.size[1]-6,pedal.size[2],...pedal.pos,dark,pedalGroup);
for(let i=0;i<5;i++){const sw=new THREE.Mesh(new THREE.CylinderGeometry(6,6,6,16),new THREE.MeshStandardMaterial({color:0xd1d4d4,metalness:.8,roughness:.3}));sw.position.set(205+60*i,pedal.pos[1]+pedal.size[1]-3,120);pedalGroup.add(sw);}label('AIRSTEP',325,113,91,pedalGroup);
box(340.4,11.5,237.6,156.8,800,50,new THREE.MeshStandardMaterial({color:0xb7bec2,metalness:.65,roughness:.35}));const screen=box(340.4,210,8,156.8,811.5,280,dark);screen.rotation.x=-.15;
// Rails are schematic envelopes: the drilling template is in the PDF.
const movingRails=new THREE.Group();scene.add(movingRails);
for(const x of [16,625.3]){box(12.7,42,300,x,71,32,metal,scene);box(5,25,300,x+3,79.5,32,metal,movingRails);}
// Guitar is an explicitly approximate fit envelope, not measured RG421 geometry.
const guitar=new THREE.Group();equipment.add(guitar);
const bodyShape=new THREE.Shape();bodyShape.moveTo(45,51);bodyShape.bezierCurveTo(10,160,10,330,90,400);bodyShape.lineTo(130,360);bodyShape.lineTo(155,505);bodyShape.lineTo(210,505);bodyShape.lineTo(240,360);bodyShape.lineTo(270,420);bodyShape.bezierCurveTo(345,330,345,170,315,51);bodyShape.closePath();
const gg=new THREE.ExtrudeGeometry(bodyShape,{depth:45,bevelEnabled:false,curveSegments:20});gg.applyMatrix4(new THREE.Matrix4().makeBasis(new THREE.Vector3(0,0,1),new THREE.Vector3(0,1,0),new THREE.Vector3(1,0,0)));gg.translate(721.5,0,0);guitar.add(new THREE.Mesh(gg,new THREE.MeshStandardMaterial({color:0x22353e,roughness:.5,side:THREE.DoubleSide})));
box(25,475,50,731.5,430,155,new THREE.MeshStandardMaterial({color:0xb19065}),guitar);box(25,125,65,731.5,905,155,dark,guitar);
function attachDetail(mesh,id){const owner=groups.find(g=>g.userData.part.id===id);owner.attach(mesh);}
for(const [id,z] of [['G1',105],['G2',205]])attachDetail(box(160,3,50,664,48,z,dark,scene),id);
// Strap passes through two slots and closes outside the neck, not around strings.
attachDetail(box(4,16,120,809,650,120,dark,scene),'GN');
for(const z of [120,240])attachDetail(box(37,16,3,774,650,z,dark,scene),'GN');
for(const x of [100,554]){const shaft=new THREE.Mesh(new THREE.CylinderGeometry(5,5,160,16),metal);shaft.rotation.x=Math.PI/2;shaft.position.set(x,720,424);scene.add(shaft);attachDetail(shaft,'U');const washer=new THREE.Mesh(new THREE.CylinderGeometry(15,15,2.5,24),metal);washer.rotation.x=Math.PI/2;washer.position.set(x,720,342.75);scene.add(washer);attachDetail(washer,'U');}
let pedalOnFloor=false;
const organizer=new THREE.Group();scene.add(organizer);const om=new THREE.MeshStandardMaterial({color:0x486c74,roughness:.8});box(120,5,100,0,0,0,om,organizer);box(120,25,5,0,5,0,om,organizer);box(120,25,5,0,5,95,om,organizer);box(5,25,90,0,5,5,om,organizer);box(5,25,90,115,5,5,om,organizer);organizer.visible=false;
$('storage').onchange=()=>{const v=$('storage').value;organizer.visible=v!=='none';organizer.position.set(...(v==='top'?[22,800,80]:v==='under'?[50,730,15]:[267,830,255]));};
function arrange(){const e=Number($('explode').value)/100;for(const g of groups){const p=g.userData.part;g.position.copy(g.userData.pivot).add(new THREE.Vector3((p.origin[0]<100?-1:1)*e*140,e*(p.origin[1]/800-.5)*280,(p.origin[2]>300?1:-1)*e*100));if(p.group==='drawer'&&trayOut)g.position.z-=300;if(p.group==='pedal'){if(pedalOnFloor)g.position.add(new THREE.Vector3(...data.mechanism.pedal_floor_delta));else if(trayOut)g.position.z-=300;}}const q=groups.find(g=>g.userData.part.id==='PB');pedalGroup.position.copy(q.position).sub(q.userData.pivot);movingRails.position.z=trayOut?-300:0;}
$('tray').onclick=()=>{trayOut=!trayOut;if(!trayOut)pedalOnFloor=false;arrange();$('tray').textContent=trayOut?'Закрыть ящик':'Открыть ящик';};$('explode').oninput=arrange;
$('pedal-floor').onclick=()=>{trayOut=true;pedalOnFloor=!pedalOnFloor;arrange();$('tray').textContent='Закрыть ящик';$('info').textContent=pedalOnFloor?'Площадка на полу. Ящик не несёт нажатие ногой.':'Площадка возвращена в открытый ящик.';};
$('reset').onclick=()=>{transform.detach();trayOut=false;pedalOnFloor=false;$('explode').value=0;for(const g of groups){g.rotation.set(0,0,0);g.userData.button.setAttribute('aria-pressed','false');g.userData.mesh.material.color.setHex(0x9e7650);}arrange();$('tray').textContent='Открыть ящик';$('info').textContent='Модель собрана. Сетка 100 мм.';};
$('mode').onchange=()=>transform.setMode($('mode').value);$('equipment').onchange=()=>equipment.visible=$('equipment').checked;$('holes').onchange=()=>marks.forEach(g=>g.visible=$('holes').checked);
function cam(x,y,z){camera.position.set(x,y,z);orbit.target.set(420,480,-80);orbit.update();}$('iso').onclick=()=>cam(1700,1250,-2100);$('front').onclick=()=>cam(420,480,-2300);$('back').onclick=()=>cam(420,480,2400);$('side').onclick=()=>cam(2700,480,-80);
const ray=new THREE.Raycaster(),mouse=new THREE.Vector2();renderer.domElement.addEventListener('dblclick',e=>{const r=renderer.domElement.getBoundingClientRect();mouse.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);ray.setFromCamera(mouse,camera);const hit=ray.intersectObjects(groups.map(g=>g.userData.mesh))[0];if(hit)select(hit.object.userData.group);});
new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}).observe(host);
$('status').textContent=`${data.parts.length} деталей · ${data.joints.length} соединений · ${data.parts.reduce((n,p)=>n+p.holes.length,0)} сверлений · D2`;renderer.setAnimationLoop(()=>{orbit.update();renderer.render(scene,camera);});
}catch(err){$('status').textContent='Не удалось загрузить модель: '+err.message+'. Проверьте интернет; открывайте через HTTP, не file://.';console.error(err);}
