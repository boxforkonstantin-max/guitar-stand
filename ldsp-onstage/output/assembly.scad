// D1, mm. Prototype: ventilation and guitar holder not released.
$fn=32;
// L Левая боковина
multmatrix([[0, 0, 1, 0], [0, 1, 0, 16], [1, 0, 0, 0], [0, 0, 0, 1]]) difference() { cube([360,768,16]);
translate([50.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 168.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 168.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 168.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 168.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 168.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 168.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 224.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 224.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 264.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 264.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 684.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 684.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 724.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 724.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([180.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([310.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
}
// R Правая боковина
multmatrix([[0, 0, 1, 638], [0, 1, 0, 16], [1, 0, 0, 0], [0, 0, 0, 1]]) difference() { cube([360,768,16]);
translate([50.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 168.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 168.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 168.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 168.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 168.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 168.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 224.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 224.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 264.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 264.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 684.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 684.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 724.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 724.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([180.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([310.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([120.0, 568.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
translate([120.0, 688.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
translate([240.0, 568.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
translate([240.0, 688.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
}
// T Площадка ноутбука
multmatrix([[1, 0, 0, 0], [0, 0, 1, 784], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { cube([654,360,16]);
translate([8.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([8.0, 180.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 180.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([8.0, 310.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 310.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([646.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([646.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([646.0, 180.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([646.0, 180.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([646.0, 310.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([646.0, 310.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
}
// D Дно корпуса
multmatrix([[1, 0, 0, 16], [0, 0, 1, 16], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { cube([622,360,16]);
translate([-0.01, 50.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 180.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 310.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 50.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 180.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 310.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([54.0, 45.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([311.0, 45.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([568.0, 45.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([54.0, 315.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([311.0, 315.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([568.0, 315.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
}
// K Полка Katana
multmatrix([[1, 0, 0, 16], [0, 0, 1, 176], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { cube([622,360,16]);
translate([-0.01, 50.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 180.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 310.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 50.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 180.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 310.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
}
// V Задняя нижняя связь
multmatrix([[1, 0, 0, 16], [0, 1, 0, 220], [0, 0, 1, 344], [0, 0, 0, 1]]) difference() { cube([622,80,16]);
translate([-0.01, 20.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 60.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 20.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 60.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
}
// U Задняя верхняя связь
multmatrix([[1, 0, 0, 16], [0, 1, 0, 680], [0, 0, 1, 344], [0, 0, 0, 1]]) difference() { cube([622,80,16]);
translate([-0.01, 20.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 60.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 20.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 60.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
}
// Q Дека съёмной кассеты
multmatrix([[1, 0, 0, 32], [0, 0, 1, 40], [0, 1, 0, 32], [0, 0, 0, 1]]) difference() { cube([590,280,16]);
translate([50.0, -0.01, 8.0]) rotate([-90, 0, 0]) cylinder(d=5,h=38.02);
translate([190.0, -0.01, 8.0]) rotate([-90, 0, 0]) cylinder(d=5,h=38.02);
translate([400.0, -0.01, 8.0]) rotate([-90, 0, 0]) cylinder(d=5,h=38.02);
translate([540.0, -0.01, 8.0]) rotate([-90, 0, 0]) cylinder(d=5,h=38.02);
translate([30.0, 30.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=10.02);
translate([30.0, 250.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=10.02);
translate([560.0, 30.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=10.02);
translate([560.0, 250.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=10.02);
hull(){
translate([225.0,220,-0.1]) cylinder(d=20,h=16.2);
translate([365.0,220,-0.1]) cylinder(d=20,h=16.2);
}
}
// F Фасад кассеты
multmatrix([[1, 0, 0, 18], [0, 1, 0, 36], [0, 0, 1, 16], [0, 0, 0, 1]]) difference() { cube([618,120,16]);
translate([64.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([64.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([204.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([204.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([414.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([414.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([554.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([554.0, 12.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
hull(){
translate([266.0,85,-0.1]) cylinder(d=24,h=16.2);
translate([352.0,85,-0.1]) cylinder(d=24,h=16.2);
}
}
// E1 Передняя опорная планка
multmatrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 20], [0, 0, 0, 1]]) difference() { cube([654,50,16]);
translate([70.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([327.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([584.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// E2 Задняя опорная планка
multmatrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 290], [0, 0, 0, 1]]) difference() { cube([654,50,16]);
translate([70.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([327.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([584.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// A Сменная плашка держателя
multmatrix([[0, 0, 1, 654], [0, 1, 0, 544], [1, 0, 0, 100], [0, 0, 0, 1]]) difference() { cube([160,200,16]);
translate([20.0, 40.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
translate([20.0, 160.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
translate([140.0, 40.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
translate([140.0, 160.0, -0.01]) rotate([0, 0, 0]) cylinder(d=6.5,h=16.02);
hull(){
translate([50,72.75,-0.1]) cylinder(d=5.5,h=16.2);
translate([50,127.25,-0.1]) cylinder(d=5.5,h=16.2);
}
hull(){
translate([110,72.75,-0.1]) cylinder(d=5.5,h=16.2);
translate([110,127.25,-0.1]) cylinder(d=5.5,h=16.2);
}
}