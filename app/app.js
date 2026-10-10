import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';

const MM = 1;
const host = document.getElementById('canvasHost');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x11171b);
scene.fog = new THREE.Fog(0x11171b, 1700, 3200);

const camera = new THREE.PerspectiveCamera(38, 1, 1, 6000);
camera.position.set(1450, 1100, -1450);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
host.appendChild(renderer.domElement);

const orbit = new OrbitControls(camera, renderer.domElement);
orbit.target.set(295, 380, 210);
orbit.enableDamping = true;
orbit.dampingFactor = 0.08;
orbit.minDistance = 450;
orbit.maxDistance = 3200;

const transform = new TransformControls(camera, renderer.domElement);
transform.setTranslationSnap(5);
transform.setRotationSnap(THREE.MathUtils.degToRad(5));
transform.setSize(0.78);
transform.addEventListener('dragging-changed', event => { orbit.enabled = !event.value; });
transform.addEventListener('objectChange', () => {syncInspector(); hideRoutingForEdit();});
scene.add(transform.getHelper());

scene.add(new THREE.HemisphereLight(0xddeeff, 0x2a2118, 2.2));
const key = new THREE.DirectionalLight(0xffffff, 3.4);
key.position.set(720, 1200, 620);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.camera.left = -1000;
key.shadow.camera.right = 1000;
key.shadow.camera.top = 1200;
key.shadow.camera.bottom = -500;
scene.add(key);

const grid = new THREE.GridHelper(2000, 20, 0x416d82, 0x27373e);
grid.position.set(295, -1, 210);
scene.add(grid);
scene.add(new THREE.AxesHelper(160));

const assembly = new THREE.Group();
assembly.name = 'Всё изделие';
scene.add(assembly);

const wood = new THREE.MeshStandardMaterial({ color: 0xc28b47, roughness: 0.62, metalness: 0.02 });
const face = new THREE.MeshStandardMaterial({ color: 0x303534, roughness: 0.92 });
const edge = new THREE.LineBasicMaterial({ color: 0x4b2d17, transparent: true, opacity: 0.78 });
const equipmentMat = new THREE.MeshStandardMaterial({ color: 0x242a2e, roughness: 0.7, metalness: 0.12 });
const screenMat = new THREE.MeshStandardMaterial({ color: 0x75c7df, emissive: 0x153844, emissiveIntensity: 0.8, roughness: 0.3 });

function bezier(p0,p1,p2,p3,steps=16) {
  const points=[];
  for (let i=0;i<steps;i++) {
    const t=i/steps, u=1-t;
    points.push([
      u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
      u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]
    ]);
  }
  return points;
}

const model = await (await fetch('../output/model.json', {cache:'no-store'})).json();
const profiles = model.profiles;
let activeProfile = model.defaultProfile;
function profilePoints() {
  return model.variants[activeProfile].polygons.B.slice(0,-2);
}

const partDefs = model.parts.map(p=>({...p,kind:p.plane==='side'?'side':'box',x:p.pos[0],rot:p.rotation,size:(p.size||[420,model.sideHeight]).join(' × ')+' × 18'}));

const parts = new Map();
const original = new Map();

function addEdges(mesh) {
  const lines = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry, 18), edge);
  mesh.add(lines);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
}

function sideGeometry() {
  const frontCurve = profilePoints();
  // ExtrudeGeometry uses ShapeUtils.triangulateShape (ear clipping), which
  // preserves the concave S-profile. A triangle fan would incorrectly fill
  // the recesses between the front-edge control points.
  const shape = new THREE.Shape();
  shape.moveTo(frontCurve[0][0], frontCurve[0][1]);
  for (const [z,y] of frontCurve.slice(1)) shape.lineTo(z,y);
  shape.lineTo(420,model.sideHeight);
  shape.lineTo(420,0);
  shape.closePath();
  const g = new THREE.ExtrudeGeometry(shape, {
    depth: 18,
    bevelEnabled: false,
    curveSegments: 1
  });
  // Shape XY = stand depth/height; extrusion Z = panel thickness.
  // Rotate into world X/Y/Z and translate so the panel spans X=0…18.
  g.rotateY(-Math.PI / 2);
  g.translate(18,0,0);
  g.computeVertexNormals();
  return g;
}

function boardGeometry(def) {
  const points=model.variants[activeProfile].polygons[def.code];
  const shape=new THREE.Shape(points.map(p=>new THREE.Vector2(...p)));
  const g=new THREE.ExtrudeGeometry(shape,{depth:18,bevelEnabled:false});
  const source=model.parts.find(p=>p.id===def.id), [w,d]=source.size;
  g.translate(-w/2,-d/2,-9);
  if(def.plane==='horizontal') g.rotateX(Math.PI/2);
  return g;
}

for (const def of partDefs) {
  let mesh;
  if (def.kind === 'side') {
    mesh = new THREE.Mesh(sideGeometry(), [face,wood]);
    mesh.position.x = def.x;
  } else {
    mesh = new THREE.Mesh(boardGeometry(def), [face,wood]);
    mesh.position.set(...def.pos);
    if (def.rot) mesh.rotation.set(...def.rot.map(THREE.MathUtils.degToRad));
  }
  mesh.name = `${def.id} · ${def.name}`;
  mesh.userData = { ...def, isPart:true };
  addEdges(mesh);
  assembly.add(mesh);
  parts.set(def.id, mesh);
  original.set(def.id, { position:mesh.position.clone(), rotation:mesh.rotation.clone() });
}

document.getElementById('profileChoice').addEventListener('change', event => {
  activeProfile = event.target.value;
  for (const id of ['B1','B2']) {
    const mesh=parts.get(id);
    mesh.geometry.dispose();
    for (const child of [...mesh.children]) { child.geometry?.dispose(); mesh.remove(child); }
    mesh.geometry=sideGeometry();
    addEdges(mesh);
  }
  syncInspector();
  updateDownloads();
});

const equipment = new THREE.Group();
equipment.name = 'Оборудование';
assembly.add(equipment);

const amp = new THREE.Mesh(new THREE.BoxGeometry(...model.equipment.amp.dims), equipmentMat);
amp.position.set(...model.equipment.amp.pos);
amp.rotation.set(...model.equipment.amp.rotation.map(THREE.MathUtils.degToRad));
amp.name = 'Boss Katana-50 MkII';
addEdges(amp);
equipment.add(amp);

const pedal = new THREE.Mesh(new THREE.BoxGeometry(...model.equipment.pedal.dims), equipmentMat);
pedal.position.set(...model.equipment.pedal.pos);
pedal.rotation.x = THREE.MathUtils.degToRad(-10);
pedal.name = 'XSONIC AIRSTEP';
addEdges(pedal);
equipment.add(pedal);

// Equipment detail is illustrative; only the nominal envelopes are dimensioned.
const metal=new THREE.MeshStandardMaterial({color:0xa6afb1,metalness:.8,roughness:.35});
const black=new THREE.MeshStandardMaterial({color:0x111314,roughness:.92});
function detailBox(parent,dims,pos,mat=black){const m=new THREE.Mesh(new THREE.BoxGeometry(...dims),mat);m.position.set(...pos);parent.add(m);return m;}
function label(parent,caption,pos,width=80,height=18,front=false){
 const canvas=document.createElement('canvas');canvas.width=512;canvas.height=128;
 const ctx=canvas.getContext('2d');ctx.fillStyle='#dbe4df';ctx.font='bold 42px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(caption,256,64);
 const texture=new THREE.CanvasTexture(canvas);const m=new THREE.Mesh(new THREE.PlaneGeometry(width,height),new THREE.MeshBasicMaterial({map:texture,transparent:true,side:THREE.DoubleSide}));m.position.set(...pos);if(front)m.rotation.y=Math.PI;parent.add(m);return m;
}
// A fine procedural woven grille, not a photographic asset.
const weave=document.createElement('canvas');weave.width=64;weave.height=64;const wc=weave.getContext('2d');wc.fillStyle='#272b2c';wc.fillRect(0,0,64,64);wc.strokeStyle='#4a5050';wc.lineWidth=1;
for(let i=0;i<64;i+=4){wc.beginPath();wc.moveTo(i,0);wc.lineTo(i,64);wc.moveTo(0,i);wc.lineTo(64,i);wc.stroke();}
const grilleTexture=new THREE.CanvasTexture(weave);grilleTexture.wrapS=grilleTexture.wrapT=THREE.RepeatWrapping;grilleTexture.repeat.set(9,7);
detailBox(amp,[438,350,3],[0,-5,-120],new THREE.MeshStandardMaterial({map:grilleTexture,roughness:1}));
label(amp,'BOSS',[0,105,-124],90,26,true);
detailBox(amp,[120,12,25],[0,196,0]);
const controlPanel=detailBox(amp,[390,2,43],[0,199,70],black);
for(let i=0;i<10;i++){const knob=new THREE.Mesh(new THREE.CylinderGeometry(5,5,8,16),metal);knob.position.set(-160+i*35,203,70);amp.add(knob);}
detailBox(amp,[400,48,3],[0,158,120]);
label(amp,'KATANA 50 • MkII',[0,188,123],180,15);
detailBox(amp,[415,225,2],[0,-50,120]);
const speaker=new THREE.Mesh(new THREE.CircleGeometry(100,64),new THREE.MeshStandardMaterial({color:0x242b2d,roughness:.95}));speaker.position.set(0,-48,122);amp.add(speaker);
const magnet=new THREE.Mesh(new THREE.CylinderGeometry(36,36,32,32),metal);magnet.rotation.x=Math.PI/2;magnet.position.set(0,-48,125);amp.add(magnet);
for(let i=0;i<5;i++){
 const foot=new THREE.Mesh(new THREE.CylinderGeometry(8,8,6,24),metal);foot.position.set(-120+i*60,23,0);pedal.add(foot);
 const led=new THREE.Mesh(new THREE.SphereGeometry(2.5,8,8),new THREE.MeshBasicMaterial({color:0x70c7ed}));led.position.set(-120+i*60,23,22);pedal.add(led);
}
label(pedal,'AIRSTEP Kat Edition',[0,0,-36],180,18,true);
const ports=[];
function port(parent,name,pos,description,usb=false){
 const mat=new THREE.MeshStandardMaterial({color:usb?0x63c6df:0xdfb77b,metalness:.5,roughness:.35});
 const m=new THREE.Mesh(usb?new THREE.BoxGeometry(14,12,6):new THREE.TorusGeometry(5,2,10,24),mat);m.position.set(...pos);m.userData.port=`${name}: ${description} Координаты на корпусе схематичны.`;parent.add(m);ports.push(m);label(parent,name,[pos[0],pos[1]+15,pos[2]+3],usb?55:62,9);return m;
}
port(amp,'AC IN',[-174,151,125],'сетевое питание; маршрут отделён от USB');
const usbAmp=port(amp,'USB-B',[0,145,125],'подключение AIRSTEP Kat Edition',true);
port(amp,'AUX',[52,145,125],'вход 3,5 мм');port(amp,'EXP',[104,145,125],'FOOT CONTROL / EXP PEDAL');port(amp,'PHONES',[165,145,125],'PHONES / REC OUT');
port(amp,'PWR AMP',[165,177,125],'POWER AMP IN, схема MkII');
const usbPedal=port(pedal,'USB-C',[85,0,38],'кабель к USB-B усилителя',true);
port(pedal,'CHARGE',[-85,0,38],'зарядка; проверить разъём и полярность по корпусу');
const cables=new THREE.Group();assembly.add(cables);cables.visible=false;
function route(points,color,r=2){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));const mesh=new THREE.Mesh(new THREE.TubeGeometry(curve,80,r,8,false),new THREE.MeshStandardMaterial({color,roughness:.65}));cables.add(mesh);}
assembly.updateMatrixWorld(true);
const ps=usbPedal.getWorldPosition(new THREE.Vector3()),pe=usbAmp.getWorldPosition(new THREE.Vector3());
route([ps.toArray(),[420,130,205],[517,175,365],[517,225,365],[517,251,365],[517,280,365],[535,330,385],[530,575,390],pe.toArray()],0x64c7dd);
route([[121,610,352],[75,590,380],[48,350,390],[48,120,410]],0xd9af75,3);
for(const y of [150,340,540]) detailBox(cables,[10,18,10],[562,y,380],metal);
const holes=new THREE.Group();assembly.add(holes);holes.visible=false;
for(const proposal of model.cableProposals){
 const board=parts.get(proposal.part),def=model.parts.find(p=>p.id===proposal.part);
 const circle=new THREE.Mesh(new THREE.RingGeometry(18,20,48),new THREE.MeshBasicMaterial({color:0x64c7dd,side:THREE.DoubleSide}));circle.rotation.x=Math.PI/2;circle.position.set(proposal.center[0]-def.size[0]/2,9.3,proposal.center[1]-def.size[1]/2);
 const group=new THREE.Group();group.position.copy(board.position);group.rotation.copy(board.rotation);group.add(circle);holes.add(group);
}
document.getElementById('toggleCables').onclick=e=>{cables.visible=!cables.visible;e.currentTarget.classList.toggle('active',cables.visible);};
document.getElementById('toggleHoles').onclick=e=>{holes.visible=!holes.visible;e.currentTarget.classList.toggle('active',holes.visible);};
document.getElementById('ampSelect').onclick=()=>select(amp);
document.getElementById('pedalSelect').onclick=()=>select(pedal);
document.getElementById('hideSelected').onclick=()=>{if(selected && selected!==assembly){selected.visible=false;transform.detach();selectionBox.visible=false;}};

const laptopBase = new THREE.Mesh(new THREE.BoxGeometry(305,9,215), equipmentMat);
laptopBase.position.set(295,809,210);
equipment.add(laptopBase);
const laptopScreen = new THREE.Mesh(new THREE.BoxGeometry(305,190,8), screenMat);
laptopScreen.position.set(295,900,310);
laptopScreen.rotation.x = THREE.MathUtils.degToRad(-12);
equipment.add(laptopScreen);

const selectionBox = new THREE.BoxHelper(undefined, 0xf1bd45);
selectionBox.visible = false;
scene.add(selectionBox);

let selected = parts.get('B1');
let exploded = 0;

function buildPartList() {
  const list = document.getElementById('partsList');
  list.innerHTML = '';
  for (const def of partDefs) {
    const button = document.createElement('button');
    button.className = 'part-row';
    button.dataset.id = def.id;
    button.innerHTML = `<span class="part-code">${def.id}</span><span class="part-copy"><span class="part-name">${def.name}</span><span class="part-size">${def.size}</span></span><span class="eye" aria-hidden="true">●</span>`;
    button.addEventListener('click', () => select(parts.get(def.id)));
    list.appendChild(button);
  }
}

function select(object) {
  selected = object;
  transform.attach(object);
  selectionBox.setFromObject(object);
  selectionBox.visible = true;
  document.getElementById('selectedName').textContent = object.name;
  document.querySelectorAll('.part-row').forEach(row => row.classList.toggle('active', row.dataset.id === object.userData.id));
  syncInspector();
}

function syncInspector() {
  if (!selected) return;
  selectionBox.setFromObject(selected);
  for (const axis of ['X','Y','Z']) document.getElementById(`pos${axis}`).value = Math.round(selected.position[axis.toLowerCase()] * 10) / 10;
  for (const axis of ['X','Y','Z']) document.getElementById(`rot${axis}`).value = Math.round(THREE.MathUtils.radToDeg(selected.rotation[axis.toLowerCase()])*10)/10;
}

function hideRoutingForEdit(){cables.visible=false;holes.visible=false;document.getElementById('toggleCables').classList.remove('active');document.getElementById('toggleHoles').classList.remove('active');}

for (const axis of ['X','Y','Z']) {
  document.getElementById(`pos${axis}`).addEventListener('change', event => {
    if (!selected) return;
    selected.position[axis.toLowerCase()] = Number(event.target.value) || 0;
    hideRoutingForEdit();
    syncInspector();
  });
}
for(const axis of ['X','Y','Z']) document.getElementById(`rot${axis}`).onchange=e=>{if(selected){selected.rotation[axis.toLowerCase()]=THREE.MathUtils.degToRad(Number(e.target.value)||0);hideRoutingForEdit();syncInspector();}};

function setMode(mode) {
  transform.setMode(mode);
  document.getElementById('moveMode').classList.toggle('active', mode === 'translate');
  document.getElementById('rotateMode').classList.toggle('active', mode === 'rotate');
  document.getElementById('moveMode').setAttribute('aria-pressed', mode === 'translate');
  document.getElementById('rotateMode').setAttribute('aria-pressed', mode === 'rotate');
}

document.getElementById('moveMode').onclick = () => setMode('translate');
document.getElementById('rotateMode').onclick = () => setMode('rotate');
document.getElementById('assemblySelect').onclick = () => select(assembly);

function resetAssembly() {
  amp.position.set(...model.equipment.amp.pos);amp.rotation.set(...model.equipment.amp.rotation.map(THREE.MathUtils.degToRad));amp.visible=true;
  pedal.position.set(...model.equipment.pedal.pos);pedal.rotation.set(-Math.PI/18,0,0);pedal.visible=true;
  equipment.visible=true;hideRoutingForEdit();
  assembly.position.set(0,0,0);
  assembly.rotation.set(0,0,0);
  for (const [id, mesh] of parts) {
    const state = original.get(id);
    mesh.position.copy(state.position);
    mesh.rotation.copy(state.rotation);
    mesh.visible=true;
  }
  exploded = 0;
  document.getElementById('explode').value = 0;
  document.getElementById('explodeValue').value = '0%';
  applyExplosion();
  select(parts.get('B1'));
}

function applyExplosion() {
  const t = exploded / 100;
  const offsets = {
    B1:[220,0,0], B2:[-220,0,0], T:[0,220,0], K:[0,0,-250],
    A:[0,-100,-180], N:[0,-120,170], U:[0,70,-160]
  };
  for (const [id, mesh] of parts) {
    const base = original.get(id).position;
    const v = offsets[id];
    mesh.position.set(base.x + v[0]*t, base.y + v[1]*t, base.z + v[2]*t);
  }
  syncInspector();
}

document.getElementById('explode').addEventListener('input', event => {
  exploded = Number(event.target.value);
  document.getElementById('explodeValue').value = `${exploded}%`;
  transform.detach();
  applyExplosion();
  transform.attach(selected);
});
document.getElementById('resetAssembly').onclick = resetAssembly;
document.getElementById('toggleEquipment').onclick = event => {
  equipment.visible = !equipment.visible;
  event.currentTarget.classList.toggle('active', equipment.visible);
};
document.getElementById('showAll').onclick = () => { for (const mesh of parts.values()) mesh.visible = true; equipment.visible = true; amp.visible=true;pedal.visible=true; };

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
renderer.domElement.addEventListener('pointerdown', event => {
  if (transform.dragging || transform.axis) return;
  const rect = renderer.domElement.getBoundingClientRect();
  pointer.x = ((event.clientX-rect.left)/rect.width)*2-1;
  pointer.y = -((event.clientY-rect.top)/rect.height)*2+1;
  raycaster.setFromCamera(pointer,camera);
  const portHit=raycaster.intersectObjects(ports,false).find(h=>h.object.parent.visible && equipment.visible);
  if(portHit){document.getElementById('portInfo').textContent=portHit.object.userData.port;transform.detach();selectionBox.visible=false;return;}
  const hit = raycaster.intersectObjects([...parts.values()], false)[0];
  if (hit) select(hit.object);
});

function cameraView(position) {
  camera.position.copy(position);
  orbit.target.set(295,380,210);
  orbit.update();
}
document.getElementById('frontView').onclick = () => cameraView(new THREE.Vector3(295,400,-2050));
document.getElementById('sideView').onclick = () => cameraView(new THREE.Vector3(2250,400,210));
document.getElementById('rearView').onclick = () => {cameraView(new THREE.Vector3(1050,850,2250));transform.detach();selectionBox.visible=false;};
document.getElementById('isoView').onclick = () => cameraView(new THREE.Vector3(1450,1100,-1450));
document.getElementById('fitView').onclick = () => cameraView(new THREE.Vector3(1450,1100,-1450));

window.addEventListener('keydown', event => {
  if (event.target instanceof HTMLInputElement) return;
  if (event.key.toLowerCase() === 'w') setMode('translate');
  if (event.key.toLowerCase() === 'e') setMode('rotate');
  if (event.key === 'Escape') transform.detach();
});

function resize() {
  const w = host.clientWidth;
  const h = host.clientHeight;
  renderer.setSize(w,h,false);
  camera.aspect = w/h;
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(host);

function animate() {
  requestAnimationFrame(animate);
  orbit.update();
  if (selectionBox.visible) selectionBox.setFromObject(selected);
  renderer.render(scene,camera);
}

buildPartList();
function updateDownloads(){
 const suffix=activeProfile==='flow'?'':'_'+activeProfile;
 document.getElementById('profileNote').textContent=profiles[activeProfile].description;
 document.getElementById('downloads').innerHTML=`<a href="../output/guitar_stand_drawings${suffix}.pdf" target="_blank">Чертежи PDF ↗</a><a href="../output/guitar_stand_layout_2440x1220${suffix}.dxf" download>Раскрой DXF ↓</a><a href="../output/guitar_stand_layout_2440x1220${suffix}.svg" target="_blank">Лист SVG ↗</a><a href="../cad/guitar_stand${suffix}.scad" download>OpenSCAD ↓</a>`;
 document.getElementById('layoutImage').src=`../output/guitar_stand_layout_2440x1220${suffix}.svg`;
}
updateDownloads();
syncInspector();selectionBox.visible=false;
resize();
animate();
