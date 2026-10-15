import assert from 'node:assert/strict';
import * as T from '../vendor/three/three.module.js';
// Geometric screening only: no load rating or physical-cable certification.
for(let deg=0;deg<=90;deg++){
 const transform=v=>new T.Vector3(...v).applyAxisAngle(new T.Vector3(1,0,0),-deg*Math.PI/180).add(new T.Vector3(0,34,-2));
 for(const v of [20,170])for(const n of [-34,-16])assert(transform([200,v,n]).y>=-1e-8,'support below floor');
 for(const v of [80,150])for(const n of [2,47]){
  const p=transform([177,v,n]);assert(p.y>=32,'pedal below floor / base');assert(p.y<220,'pedal hits shelf');assert(p.z<90,'pedal hits relocated front beam');
 }
 const start=transform([177,155,25]),moving=transform([70,155,25]);
 const curve=new T.CatmullRomCurve3([start,moving,new T.Vector3(55,95,45),new T.Vector3(55,85,155),new T.Vector3(70,100,220)],false,'centripetal');
 for(const p of curve.getPoints(300)){
  assert(p.y>36.5,'cable touches base or hinge');assert(p.x>20&&p.x<634,'cable touches side');
  assert(!(p.z>87.5&&p.z<108.5&&p.y>137.5),'cable touches relocated front beam');
 }
}
assert(Math.abs(34-16-18)<1e-9,'feet must meet floor');
console.log('PASS: 91 flap angles; pedal envelope, floor support, schematic cable clearance. Physical cable length/bend radius, hinges and loads NOT certified.');
