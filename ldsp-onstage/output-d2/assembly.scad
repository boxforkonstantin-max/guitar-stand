// D2 mm. Screening only; see release holds in PDF.
$fn=64;
// L
multmatrix([[0, 0, 1, 0], [0, 1, 0, 16], [1, 0, 0, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [360, 0], [360, 768], [0, 768]]);
translate([50.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 212.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 212.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 212.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 212.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 212.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 212.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 246.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 246.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 286.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 286.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 684.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 684.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 724.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 724.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([8.0, 139.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 139.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([8.0, 189.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 189.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 139.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 139.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 189.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 189.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([180.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([310.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([64.0, 76.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([203.5, 76.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// R
multmatrix([[0, 0, 1, 638], [0, 1, 0, 16], [1, 0, 0, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [360, 0], [360, 768], [0, 768]]);
translate([50.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 212.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([50.0, 212.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([180.0, 212.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([180.0, 212.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([310.0, 212.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([310.0, 212.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 246.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 246.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 286.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 286.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 684.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 684.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 724.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 724.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([8.0, 139.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 139.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([8.0, 189.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([8.0, 189.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 139.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 139.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([352.0, 189.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([352.0, 189.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([50.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([180.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([310.0, 768.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([108.0, 562.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([108.0, 562.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([108.0, 606.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([108.0, 606.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([252.0, 562.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([252.0, 562.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([252.0, 606.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([252.0, 606.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([64.0, 76.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
translate([203.5, 76.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
}
// T
multmatrix([[1, 0, 0, 0], [0, 0, 1, 784], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [654, 0], [654, 360], [0, 360]]);
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
// D
multmatrix([[1, 0, 0, 16], [0, 0, 1, 16], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [622, 0], [622, 360], [0, 360]]);
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
// K
multmatrix([[1, 0, 0, 16], [0, 0, 1, 220], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [622, 0], [622, 360], [0, 360]]);
translate([-0.01, 50.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 180.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 310.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 50.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 180.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 310.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([84.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([234.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([384.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([534.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([84.0, 352.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([234.0, 352.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([384.0, 352.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([534.0, 352.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
}
// KF
multmatrix([[1, 0, 0, 16], [0, 1, 0, 140], [0, 0, 1, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [622, 0], [622, 80], [0, 80]]);
translate([-0.01, 15.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 65.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 15.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 65.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([84.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
translate([234.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
translate([384.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
translate([534.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
}
// KR
multmatrix([[1, 0, 0, 16], [0, 1, 0, 140], [0, 0, 1, 344], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [622, 0], [622, 80], [0, 80]]);
translate([-0.01, 15.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 65.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 15.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 65.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([84.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
translate([234.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
translate([384.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
translate([534.0, 80.01, 8.0]) rotate([90, 0, 0]) cylinder(d=2.5,h=12.02);
}
// V
multmatrix([[1, 0, 0, 16], [0, 1, 0, 242], [0, 0, 1, 344], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [622, 0], [622, 80], [0, 80]]);
translate([-0.01, 20.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 60.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 20.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 60.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
}
// U
multmatrix([[1, 0, 0, 16], [0, 1, 0, 680], [0, 0, 1, 344], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [622, 0], [622, 80], [0, 80]]);
translate([84.0, 40.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
translate([538.0, 40.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
translate([-0.01, 20.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 60.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 20.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([622.01, 60.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
}
// W100_1
multmatrix([[1, 0, 0, 75], [0, 1, 0, 695], [0, 0, 1, 360], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [50, 0], [50, 50], [0, 50]]);
translate([25.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
}
// W100_2
multmatrix([[1, 0, 0, 75], [0, 1, 0, 695], [0, 0, 1, 376], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [50, 0], [50, 50], [0, 50]]);
translate([25.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
}
// W100_3
multmatrix([[1, 0, 0, 75], [0, 1, 0, 695], [0, 0, 1, 392], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [50, 0], [50, 50], [0, 50]]);
translate([25.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
}
// W554_1
multmatrix([[1, 0, 0, 529], [0, 1, 0, 695], [0, 0, 1, 360], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [50, 0], [50, 50], [0, 50]]);
translate([25.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
}
// W554_2
multmatrix([[1, 0, 0, 529], [0, 1, 0, 695], [0, 0, 1, 376], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [50, 0], [50, 50], [0, 50]]);
translate([25.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
}
// W554_3
multmatrix([[1, 0, 0, 529], [0, 1, 0, 695], [0, 0, 1, 392], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [50, 0], [50, 50], [0, 50]]);
translate([25.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=11,h=16.02);
}
// E1
multmatrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 20], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [834, 0], [834, 50], [0, 50]]);
translate([70.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([327.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([584.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([700.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([790.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// E2
multmatrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 290], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [834, 0], [834, 50], [0, 50]]);
translate([70.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([327.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([584.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([700.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([790.0, 25.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// GB
multmatrix([[1, 0, 0, 654], [0, 0, 1, 16], [0, 1, 0, 0], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [180, 0], [180, 360], [0, 360]]);
translate([46.0, 45.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([136.0, 45.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([46.0, 315.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([136.0, 315.0, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([46.0, 130.0, -0.01]) rotate([0, 0, 0]) cylinder(d=4.5,h=16.02);
translate([136.0, 130.0, -0.01]) rotate([0, 0, 0]) cylinder(d=4.5,h=16.02);
translate([46.0, 230.0, -0.01]) rotate([0, 0, 0]) cylinder(d=4.5,h=16.02);
translate([136.0, 230.0, -0.01]) rotate([0, 0, 0]) cylinder(d=4.5,h=16.02);
}
// G1
multmatrix([[1, 0, 0, 664], [0, 0, 1, 32], [0, 1, 0, 105], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [160, 0], [160, 50], [0, 50]]);
translate([36.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
translate([126.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
}
// G2
multmatrix([[1, 0, 0, 664], [0, 0, 1, 32], [0, 1, 0, 205], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [160, 0], [160, 50], [0, 50]]);
translate([36.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
translate([126.0, 25.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
}
// GN
multmatrix([[1, 0, 0, 654], [0, 0, 1, 650], [0, 1, 0, 100], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [160, 0], [160, 47], [85, 47], [85.0, 47.0], [82.41084984098111, 47.10172798680678], [79.83766265367238, 47.40628476036046], [77.29630299275513, 47.91179262687667], [74.80243918562674, 48.61513496225993], [72.37144673195203, 49.51197542712754], [70.01831350859496, 50.59678470178386], [67.75754736437369, 51.86287457631495], [65.60308667434839, 53.30243918562674], [63.568214405103944, 54.90660313519898], [61.665476220843935, 56.66547622084393], [59.90660313519898, 58.56821440510394], [58.30243918562674, 60.60308667434838], [56.86287457631496, 62.757547364373686], [55.59678470178386, 65.01831350859496], [54.51197542712754, 67.37144673195203], [53.61513496225993, 69.80243918562672], [52.911792626876675, 72.29630299275512], [52.40628476036046, 74.83766265367238], [52.10172798680678, 77.41084984098111], [52.0, 80.0], [52.10172798680678, 82.58915015901889], [52.40628476036046, 85.16233734632762], [52.91179262687667, 87.70369700724487], [53.61513496225993, 90.19756081437326], [54.51197542712754, 92.62855326804797], [55.59678470178386, 94.98168649140504], [56.86287457631495, 97.24245263562631], [58.30243918562674, 99.39691332565161], [59.90660313519898, 101.43178559489606], [61.66547622084393, 103.33452377915606], [63.56821440510392, 105.09339686480101], [65.60308667434839, 106.69756081437326], [67.75754736437369, 108.13712542368505], [70.01831350859496, 109.40321529821614], [72.37144673195202, 110.48802457287246], [74.80243918562672, 111.38486503774007], [77.29630299275513, 112.08820737312334], [79.83766265367238, 112.59371523963955], [82.4108498409811, 112.89827201319322], [85.0, 113.0], [160, 113], [160, 160], [0, 160]]);
translate([56.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([56.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([136.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([136.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([56.0, 152.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([56.0, 152.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([136.0, 152.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([136.0, 152.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
hull(){
translate([120,11.5,-.01]) cylinder(d=5,h=16.02);
translate([120,28.5,-.01]) cylinder(d=5,h=16.02);
}
hull(){
translate([120,131.5,-.01]) cylinder(d=5,h=16.02);
translate([120,148.5,-.01]) cylinder(d=5,h=16.02);
}
}
// GC1
multmatrix([[1, 0, 0, 654], [0, 1, 0, 550], [0, 0, 1, 100], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [160, 0], [160, 100], [0, 100]]);
translate([-0.01, 28.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 72.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([56.0, 100.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([136.0, 100.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
}
// GC2
multmatrix([[1, 0, 0, 654], [0, 1, 0, 550], [0, 0, 1, 244], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [160, 0], [160, 100], [0, 100]]);
translate([-0.01, 28.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 72.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([56.0, 100.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
translate([136.0, 100.01, 8.0]) rotate([90, 0, 0]) cylinder(d=5,h=38.02);
}
// QL
multmatrix([[0, 0, 1, 28.7], [0, 1, 0, 42], [1, 0, 0, 32], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [300, 0], [300, 90], [0, 90]]);
translate([43.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([43.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([143.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([143.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([253.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([253.0, 8.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([-0.01, 22.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 72.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([72.0, 50.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
translate([200.0, 50.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
translate([264.0, 50.0, -0.01]) rotate([0, 0, 0]) cylinder(d=2.5,h=12.02);
}
// QR
multmatrix([[0, 0, 1, 609.3], [0, 1, 0, 42], [1, 0, 0, 32], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [300, 0], [300, 90], [0, 90]]);
translate([43.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([43.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([143.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([143.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([253.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d=7,h=16.02);
translate([253.0, 8.0, 16.01]) rotate([180, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([-0.01, 22.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 72.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([72.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([200.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([264.0, 50.0, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// QB
multmatrix([[1, 0, 0, 44.7], [0, 0, 1, 42], [0, 1, 0, 32], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [564.6, 0], [564.6, 300], [0, 300]]);
translate([-0.01, 43.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 143.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([-0.01, 253.0, 8.0]) rotate([0, 90, 0]) cylinder(d=5,h=38.02);
translate([564.61, 43.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([564.61, 143.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
translate([564.61, 253.0, 8.0]) rotate([0, -90, 0]) cylinder(d=5,h=38.02);
}
// F
multmatrix([[1, 0, 0, 18], [0, 1, 0, 36], [0, 0, 1, 16], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [618, 0], [618, 100], [0, 100]]);
translate([18.7, 28.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([18.7, 28.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([18.7, 78.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([18.7, 78.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([599.3, 28.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([599.3, 28.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
translate([599.3, 78.0, -0.01]) rotate([0, 0, 0]) cylinder(d=7,h=16.02);
translate([599.3, 78.0, -0.01]) rotate([0, 0, 0]) cylinder(d1=10,d2=7,h=1.5);
hull(){
translate([266.0,72,-.01]) cylinder(d=24,h=16.02);
translate([352.0,72,-.01]) cylinder(d=24,h=16.02);
}
}
// PB
multmatrix([[1, 0, 0, 77], [0, 0, 1, 74], [0, 1, 0, 65], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [500, 0], [500, 220], [0, 220]]);
translate([50.0, 22.5, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([250.0, 22.5, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([450.0, 22.5, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([50.0, 197.5, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([250.0, 197.5, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
translate([450.0, 197.5, 16.01]) rotate([180, 0, 0]) cylinder(d=4.5,h=16.02);
hull(){
translate([194.0,150,-.01]) cylinder(d=18,h=16.02);
translate([306.0,150,-.01]) cylinder(d=18,h=16.02);
}
}
// PF1
multmatrix([[1, 0, 0, 77], [0, 0, 1, 58], [0, 1, 0, 70], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [500, 0], [500, 35], [0, 35]]);
translate([50.0, 17.5, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([250.0, 17.5, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([450.0, 17.5, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}
// PF2
multmatrix([[1, 0, 0, 77], [0, 0, 1, 58], [0, 1, 0, 245], [0, 0, 0, 1]]) difference() { linear_extrude(16) polygon([[0, 0], [500, 0], [500, 35], [0, 35]]);
translate([50.0, 17.5, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([250.0, 17.5, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
translate([450.0, 17.5, 16.01]) rotate([180, 0, 0]) cylinder(d=2.5,h=12.02);
}