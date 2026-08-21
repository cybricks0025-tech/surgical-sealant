// ==============================================================================
// 創新雙腔注射器高剪切微流控混合頭 (SLA / DLP 3D 列印參數化模型)
// 設計目標：解決高黏度 PEG (S-buffer) 與水狀 T-buffer 黏度差，2-3 秒內快速成膠，避開 3D 燒結多孔專利
// 適用列印精度：XY 解析度 25-50 um, Z 層厚 25-50 um (如 Formlabs 4 / Elegoo Saturn / Anycubic 等)
// ==============================================================================

$fn = 60; // 圓弧細分度

// 1. 全域尺寸參數定義 (單位：mm)
luer_spacing      = 9.5;    // 標準雙聯針筒中心孔距 (mm)
luer_inner_dia_a  = 2.8;    // A 通道 (PEG-S, 高黏度) 接收孔內徑
luer_inner_dia_b  = 2.8;    // B 通道 (T-buffer, 水狀) 接收孔內徑
luer_outer_dia    = 5.6;    // Luer 接頭外徑
luer_length       = 6.0;    // Luer 接頭高度

// 歧管與流阻平衡參數
orifice_dia_peg   = 0.80;   // PEG 阻尼孔徑 (mm) - 降低流阻
orifice_dia_tbuf  = 0.35;   // T-buffer 阻尼孔徑 (mm) - 增加微流阻以平衡黏度推力

// 主混合腔體尺寸
chamber_width     = 2.4;    // 矩形流道寬度 (mm)
chamber_height    = 0.6;    // 矩形流道高度 (mm)
chamber_length    = 8.0;    // 人字形混練區長度 (mm)

// 人字形微溝槽 (SHM) 參數
shm_groove_depth  = 0.08;   // 溝槽深度 80 um (0.08 mm)
shm_groove_width  = 0.15;   // 溝槽寬度 150 um (0.15 mm)
shm_pitch         = 0.35;   // 溝槽間距 (mm)
shm_angle         = 45;     // 人字形夾角 (度)
shm_ratio         = 0.67;   // 非對稱比例 (2:1 偏置，引發混沌雙渦旋)

// 淚滴形微阻流島 (Shear Pillar) 參數
pillar_width      = 0.20;   // 微柱寬度 (mm)
pillar_length     = 0.40;   // 微柱長度 (mm)
pillar_gap        = 0.12;   // 柱間剪切狹縫 (120 um)
pillar_rows       = 3;      // 剪切微柱排數

// 噴嘴出口與外殼參數
nozzle_exit_dia   = 1.0;    // 最終噴嘴出料孔徑 (mm)
nozzle_length     = 3.0;    // 噴嘴段長度 (mm)
housing_wall      = 1.5;    // 外壁保護厚度 (mm)

module luer_inlets() {
    difference() {
        union() {
            translate([-luer_spacing/2, 0, 0])
                cylinder(d=luer_outer_dia, h=luer_length);
            translate([luer_spacing/2, 0, 0])
                cylinder(d=luer_outer_dia, h=luer_length);
            translate([-luer_spacing/2, -luer_outer_dia/2, 0])
                cube([luer_spacing, luer_outer_dia, luer_length]);
        }
        translate([-luer_spacing/2, 0, -0.1])
            cylinder(d1=luer_inner_dia_a + 0.3, d2=luer_inner_dia_a, h=luer_length + 0.2);
        translate([luer_spacing/2, 0, -0.1])
            cylinder(d1=luer_inner_dia_b + 0.3, d2=luer_inner_dia_b, h=luer_length + 0.2);
    }
}

module fluid_internal_channels() {
    union() {
        hull() {
            translate([-luer_spacing/2, 0, luer_length-0.1])
                cylinder(d=luer_inner_dia_a, h=0.1);
            translate([-0.4, 0, luer_length + 2.0])
                cylinder(d=orifice_dia_peg, h=0.5);
        }
        hull() {
            translate([luer_spacing/2, 0, luer_length-0.1])
                cylinder(d=luer_inner_dia_b, h=0.1);
            translate([0.4, 0, luer_length + 2.0])
                cylinder(d=orifice_dia_tbuf, h=0.5);
        }
        translate([-chamber_width/2, -chamber_height/2, luer_length + 2.5])
            cube([chamber_width, chamber_height, 0.5]);
        translate([-chamber_width/2, -chamber_height/2, luer_length + 3.0])
            cube([chamber_width, chamber_height, chamber_length]);
        translate([-chamber_width/2, -chamber_height/2, luer_length + 3.0 + chamber_length])
            cube([chamber_width, chamber_height, 2.0]);
        hull() {
            translate([-chamber_width/2, -chamber_height/2, luer_length + 5.0 + chamber_length])
                cube([chamber_width, chamber_height, 0.1]);
            translate([0, 0, luer_length + 5.0 + chamber_length + nozzle_length])
                cylinder(d=nozzle_exit_dia, h=0.1);
        }
    }
}

module shm_groove_inserts() {
    z_start = luer_length + 3.0;
    for (i = [0 : 1 : floor(chamber_length / shm_pitch) - 1]) {
        z_pos = z_start + i * shm_pitch;
        apex_x = -chamber_width/2 + chamber_width * shm_ratio;
        translate([0, -chamber_height/2 + shm_groove_depth/2, z_pos]) {
            rotate([0, shm_angle, 0])
                cube([chamber_width*0.7, shm_groove_depth, shm_groove_width], center=true);
            translate([apex_x, 0, 0])
                rotate([0, -shm_angle, 0])
                    cube([chamber_width*0.4, shm_groove_depth, shm_groove_width], center=true);
        }
    }
}

module shear_pillars() {
    z_base = luer_length + 3.0 + chamber_length + 0.3;
    for (r = [0 : pillar_rows - 1]) {
        z_row = z_base + r * (pillar_length + 0.3);
        x_offset = (r % 2 == 0) ? -0.5 : 0.5;
        for (c = [-1, 0, 1]) {
            translate([c * (pillar_width + pillar_gap*2) + x_offset*0.3, 0, z_row]) {
                cylinder(d=pillar_width, h=chamber_height, center=true);
                translate([0, 0, -pillar_length/4])
                    cylinder(d1=pillar_width, d2=0.05, h=pillar_length/2, center=true);
            }
        }
    }
}

module novel_mixing_tip_assembly() {
    total_body_length = luer_length + 5.0 + chamber_length + nozzle_length;
    difference() {
        union() {
            luer_inlets();
            hull() {
                translate([-luer_spacing/2, -luer_outer_dia/2, luer_length - 0.5])
                    cube([luer_spacing, luer_outer_dia, 1.0]);
                translate([-chamber_width/2 - housing_wall, -chamber_height/2 - housing_wall, luer_length + 2.0])
                    cube([chamber_width + housing_wall*2, chamber_height + housing_wall*2, chamber_length + 3.0]);
            }
            hull() {
                translate([-chamber_width/2 - housing_wall, -chamber_height/2 - housing_wall, luer_length + 5.0 + chamber_length])
                    cube([chamber_width + housing_wall*2, chamber_height + housing_wall*2, 0.5]);
                translate([0, 0, total_body_length])
                    cylinder(d=nozzle_exit_dia + housing_wall*2, h=0.5);
            }
        }
        fluid_internal_channels();
    }
    intersection() {
        translate([-chamber_width/2, -chamber_height/2, luer_length + 3.0])
            cube([chamber_width, chamber_height, chamber_length + 2.0]);
        union() {
            shm_groove_inserts();
            shear_pillars();
        }
    }
}

novel_mixing_tip_assembly();
